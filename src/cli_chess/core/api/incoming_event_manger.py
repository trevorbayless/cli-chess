from cli_chess.utils.event import Event, EventTopics
from cli_chess.utils.logging import log
from typing import Callable
from enum import Enum, auto
from types import MappingProxyType
import threading


class IEMEventTopics(Enum):
    CHALLENGE = auto()  # A challenge sent by us or to us
    CHALLENGE_CANCELLED = auto()
    CHALLENGE_DECLINED = auto()
    NOT_IMPLEMENTED = auto()


iem_type_to_event_dict = MappingProxyType({
    "gameStart": EventTopics.GAME_START,
    "gameFinish": EventTopics.GAME_END,
    "challenge": IEMEventTopics.CHALLENGE,
    "challengeCanceled": IEMEventTopics.CHALLENGE_CANCELLED,
    "challengeDeclined": IEMEventTopics.CHALLENGE_DECLINED,
})


class IncomingEventManager(threading.Thread):
    """Opens a stream and keeps track of Lichess incoming
       events (such as game start, game finish).
    """

    def __init__(self):
        super().__init__(daemon=True)
        self.e_new_event_received = Event()
        self.my_games = []

    def run(self) -> None:
        try:
            from cli_chess.core.api.api_manager import api_client
        except ImportError:
            # TODO: Clean this up so the error is displayed on the main screen
            log.error("Failed to import api_client")
            raise ImportError("API client not setup. Do you have an API token linked?")

        log.info("Started listening to Lichess incoming events")
        for event in api_client.board.stream_incoming_events():
            data = None
            event_topic = iem_type_to_event_dict.get(event['type'], IEMEventTopics.NOT_IMPLEMENTED)
            log.debug(f"IEM event received: {event}")

            if event_topic is EventTopics.GAME_START:
                data = event['game']
                self.my_games.append(data['gameId'])

            elif event_topic is EventTopics.GAME_END:
                try:
                    data = event['game']
                    self.my_games.remove(data['gameId'])
                except ValueError:
                    pass

            elif (event_topic is IEMEventTopics.CHALLENGE or
                  event_topic is IEMEventTopics.CHALLENGE_CANCELLED or
                  event_topic is IEMEventTopics.CHALLENGE_DECLINED):
                data = event['challenge']

            self.e_new_event_received.notify(event_topic, data=data)

    def get_active_games(self) -> list:
        """Returns a list of games in progress for this account"""
        return self.my_games

    def subscribe_to_events(self, listener: Callable) -> None:
        """Subscribes the passed in method to IEM events"""
        self.e_new_event_received.add_listener(listener)

    def unsubscribe_from_events(self, listener: Callable) -> None:
        """Unsubscribes the passed in method to IEM events"""
        self.e_new_event_received.remove_listener(listener)
