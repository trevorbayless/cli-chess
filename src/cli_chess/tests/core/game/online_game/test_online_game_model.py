from cli_chess.core.game.game_options import GameOption
from cli_chess.core.game.online_game import OnlineGameModel
from cli_chess.core.api.incoming_event_manger import IEMEventTopics
from cli_chess.utils import EventTopics
from chess import WHITE, BLACK
from unittest.mock import Mock
import threading
import pytest


@pytest.fixture
def model(monkeypatch):
    from cli_chess.core.api import api_manager
    monkeypatch.setattr(api_manager, "api_client", Mock(), raising=False)
    monkeypatch.setattr(api_manager, "api_iem", Mock(), raising=False)

    game_parameters = {
        GameOption.COLOR: "random",
        GameOption.VARIANT: "standard",
        GameOption.TIME_CONTROL: (10, 5),
        GameOption.RATED: False,
        GameOption.OPPONENT: "testOpponent",
    }
    return OnlineGameModel(game_parameters, is_vs_ai=False)


def test_create_game_sends_direct_challenge(model):
    model.api_client.challenges.create.return_value = {'id': 'abc123'}
    challenge_sent = threading.Event()
    received = {}

    def listener(*args, **kwargs):
        if kwargs.get('msg'):
            received.update(args=args, msg=kwargs.get('msg'))
            challenge_sent.set()

    model.e_game_model_updated.add_listener(listener)
    model.create_game()

    assert challenge_sent.wait(timeout=5)
    model.api_client.challenges.create.assert_called_once_with(username="testOpponent",
                                                               rated=False,
                                                               clock_limit=600,
                                                               clock_increment=5,
                                                               color="random",
                                                               variant="standard")
    assert model.sent_challenge_id == 'abc123'
    assert EventTopics.GAME_SEARCH in received['args']
    assert received['msg'] == "Challenge sent to testOpponent. Waiting for a response..."


def test_iem_challenge_declined_stops_search(model):
    received = {}

    def listener(*args, **kwargs):
        received.update(args=args, msg=kwargs.get('msg'))

    model.e_game_model_updated.add_listener(listener)
    model.searching = True
    model.sent_challenge_id = 'abc123'
    model._handle_iem_event(IEMEventTopics.CHALLENGE_DECLINED, data={'id': 'abc123', 'declineReason': 'Too fast'})

    assert not model.searching
    assert model.sent_challenge_id is None
    assert EventTopics.ERROR in received['args']
    assert received['msg'] == 'Too fast'


def test_iem_challenge_declined_other_id_ignored(model):
    received = {}

    def listener(*args, **kwargs):
        received.update(args=args, msg=kwargs.get('msg'))

    model.e_game_model_updated.add_listener(listener)
    model.searching = True
    model.sent_challenge_id = 'abc123'
    model._handle_iem_event(IEMEventTopics.CHALLENGE_DECLINED, data={'id': 'zzz999'})

    assert model.searching
    assert model.sent_challenge_id == 'abc123'
    assert not received


def test_iem_challenge_cancelled_stops_search(model):
    received = {}

    def listener(*args, **kwargs):
        received.update(args=args, msg=kwargs.get('msg'))

    model.e_game_model_updated.add_listener(listener)
    model.searching = True
    model.sent_challenge_id = 'abc123'
    model._handle_iem_event(IEMEventTopics.CHALLENGE_CANCELLED, data={'id': 'abc123'})

    assert not model.searching
    assert EventTopics.ERROR in received['args']
    assert received['msg'] == "The challenge has been cancelled"


def test_exit_cancels_pending_challenge(model):
    model.searching = True
    model.sent_challenge_id = 'abc123'
    model.exit()

    model.api_client.challenges.cancel.assert_called_once_with('abc123')
    assert not model.game_in_progress
    assert model.sent_challenge_id is None


def test_exit_without_pending_challenge(model):
    model.exit()

    model.api_client.challenges.cancel.assert_not_called()
    assert not model.game_in_progress


def game_full_event_data(moves: str = "") -> dict:
    return {
        'white': {'name': "testWhite", 'rating': 1500},
        'black': {'name': "testBlack", 'rating': 1500},
        'state': {'moves': moves, 'wtime': 180000, 'btime': 180000, 'winc': 2000, 'binc': 2000},
    }


def test_game_start_saves_initial_clock_time(model):
    model._handle_gsd_event(EventTopics.GAME_START, data=game_full_event_data())

    assert model.game_metadata.clocks[WHITE].initial_time == 180000
    assert model.game_metadata.clocks[BLACK].initial_time == 180000


def test_initial_clock_time_is_kept_as_moves_are_made(model):
    model._handle_gsd_event(EventTopics.GAME_START, data=game_full_event_data())
    model._handle_gsd_event(EventTopics.MOVE_MADE, data={'moves': "e2e4 e7e5", 'wtime': 37000, 'btime': 42000})

    assert model.game_metadata.clocks[WHITE].time == 37000
    assert model.game_metadata.clocks[WHITE].initial_time == 180000
