from cli_chess.utils.event import Event
from cli_chess.utils.logging import log
from typing import Callable
import threading


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
            if event['type'] == 'gameStart':
                game_id = event['game']['gameId']
                log.info(f"Received gameStart for: {game_id}")
                self.my_games.append(game_id)
                self.e_new_event_received.notify(gameStart=event)

            elif event['type'] == 'gameFinish':
                game_id = event['game']['gameId']
                try:
                    self.my_games.remove(event['game']['gameId'])
                except ValueError:
                    pass

                log.info(f"Received gameEnd for: {game_id}")
                self.e_new_event_received.notify(gameFinish=event)

            elif event['type'] == 'challenge':
                # A challenge was sent by us or to us
                challenge_id = event['challenge']['id']
                log.info(f"Received challenge event for: {challenge_id}")
                self.e_new_event_received.notify(challenge=event)

            elif event['type'] == 'challengeCanceled':
                challenge_id = event['challenge']['id']
                log.info(f"Received challengeCanceled event for: {challenge_id}")
                self.e_new_event_received.notify(challengeCanceled=event)

            elif event['type'] == 'challengeDeclined':
                challenge_id = event['challenge']['id']
                log.info(f"Received challengeDeclined event for: {challenge_id}")
                self.e_new_event_received.notify(challengeCanceled=event)

            else:
                log.info(f"Received other event: {event}")
                self.e_new_event_received.notify(other=event)

    def get_active_games(self) -> list:
        """Returns a list of games in progress for this account"""
        return self.my_games

    def subscribe_to_events(self, listener: Callable) -> None:
        """Subscribes the passed in method to IEM events"""
        self.e_new_event_received.add_listener(listener)

    def unsubscribe_from_events(self, listener: Callable) -> None:
        """Unsubscribes the passed in method to IEM events"""
        self.e_new_event_received.remove_listener(listener)
