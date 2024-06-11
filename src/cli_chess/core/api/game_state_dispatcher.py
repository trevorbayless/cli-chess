from cli_chess.utils import Event, EventTopics, log, retry
from typing import Callable
from threading import Thread
from enum import Enum, auto
from types import MappingProxyType


class GSDEventTopics(Enum):
    CHAT_RECEIVED = auto()
    OPPONENT_GONE = auto()
    NOT_IMPLEMENTED = auto()


gsd_type_to_event_dict = MappingProxyType({
    "gameFull": EventTopics.GAME_START,
    "gameState": EventTopics.MOVE_MADE,
    "chatLine": GSDEventTopics.CHAT_RECEIVED,
    "opponentGone": GSDEventTopics.OPPONENT_GONE,
})


class GameStateDispatcher(Thread):
    """Handles streaming a game and sending game commands (make move, offer draw, etc)
       using the Board API. The game that is streamed using this class must be owned
       by the account linked to the api token.
    """
    def __init__(self, game_id=""):
        super().__init__()
        self.game_id = game_id
        self.is_game_over = False
        self.e_game_state_dispatcher_event = Event()

        try:
            from cli_chess.core.api.api_manager import api_client
            self.api_client = api_client
        except ImportError:
            # TODO: Clean this up so the error is displayed on the main screen
            log.error("Failed to import api_client")
            raise ImportError("API client not setup. Do you have an API token linked?")

    def run(self):
        """This is the threads main function. It handles emitting the game state to
           listeners (typically the OnlineGameModel).
        """
        log.info(f"Started streaming game state: {self.game_id}")

        for event in self.api_client.board.stream_game_state(self.game_id):
            event_topic = gsd_type_to_event_dict.get(event['type'], GSDEventTopics.NOT_IMPLEMENTED)
            log.debug(f"GSD Stream event type received: {event['type']} // topic: {event_topic}")

            if event_topic is EventTopics.MOVE_MADE:
                status = event.get('status', None)
                self.is_game_over = status and status != "started" and status != "created"

            elif event_topic is GSDEventTopics.OPPONENT_GONE:
                is_gone = event.get('gone', False)
                secs_until_claim = event.get('claimWinInSeconds', None)

                if is_gone and secs_until_claim:
                    pass  # TODO implement call to auto-claim win when `secs_until_claim` elapses

                if not is_gone:
                    pass  # TODO: Cancel auto-claim countdown

            game_end_event = EventTopics.GAME_END if self.is_game_over else None
            self.e_game_state_dispatcher_event.notify(event_topic, game_end_event, data=event)

            if self.is_game_over:
                self._game_ended()

        log.info(f"Completed streaming of: {self.game_id}")

    @retry(times=3, exceptions=(Exception, ))
    def make_move(self, move: str):
        """Sends the move to lichess. This move should have already
           been verified as valid in the current context of the board.
           The move must be in UCI format.
        """
        log.debug(f"Sending move ({move}) to lichess")
        self.api_client.board.make_move(self.game_id, move)

    @retry(times=3, exceptions=(Exception,))
    def send_takeback_request(self) -> None:
        """Sends a takeback request to our opponent"""
        log.debug("Sending takeback offer to opponent")
        self.api_client.board.offer_takeback(self.game_id)

    @retry(times=3, exceptions=(Exception,))
    def send_draw_offer(self) -> None:
        """Sends a draw offer to our opponent"""
        log.debug("Sending draw offer to opponent")
        self.api_client.board.offer_draw(self.game_id)

    @retry(times=3, exceptions=(Exception,))
    def resign(self) -> None:
        """Resigns the game"""
        log.debug("Sending resignation")
        self.api_client.board.resign_game(self.game_id)

    @retry(times=3, exceptions=(Exception,))
    def claim_victory(self) -> None:
        """Submits a claim of victory to lichess as the opponent is gone.
           This is to only be called when the opponentGone timer has elapsed.
        """
        pass

    def _game_ended(self) -> None:
        """Handles removing all event listeners since the game has completed"""
        log.info("GAME ENDED: Removing existing GSD listeners")
        self.is_game_over = True
        self.e_game_state_dispatcher_event.remove_all_listeners()

    def subscribe_to_events(self, listener: Callable) -> None:
        """Subscribes the passed in method to GSD events"""
        self.e_game_state_dispatcher_event.add_listener(listener)
