from cli_chess.utils import Event, log, retry
from typing import Callable
from threading import Thread


class GameStateDispatcher(Thread):
    """Handles streaming a game and sending game commands (make move, offer draw, etc)
       using the Board API. The game that is streamed using this class must be owned
       by the account linked to the api token.
    """

    def __init__(self, game_id=""):
        super().__init__()
        self.game_id = game_id
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
            log.debug(f"Stream event received: {event['type']}")
            if event['type'] == "gameFull":
                self.e_game_state_dispatcher_event.notify(gameFull=event)

            elif event['type'] == "gameState":
                status = event.get('status', None)
                is_game_over = status and status != "started" and status != "created"

                self.e_game_state_dispatcher_event.notify(gameState=event, gameOver=is_game_over)
                if is_game_over:
                    self._game_ended()

            elif event['type'] == "chatLine":
                self.e_game_state_dispatcher_event.notify(chatLine=event)

            elif event['type'] == "opponentGone":
                is_gone = event.get('gone', False)
                secs_until_claim = event.get('claimWinInSeconds', None)

                if is_gone and secs_until_claim:
                    pass  # TODO implement call to auto-claim win when `secs_until_claim` elapses

                if not is_gone:
                    pass  # TODO: Cancel auto-claim countdown

                self.e_game_state_dispatcher_event.notify(opponentGone=event)

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
        self.e_game_state_dispatcher_event.remove_all_listeners()

    def subscribe_to_events(self, listener: Callable) -> None:
        """Subscribes the passed in method to GSD events"""
        self.e_game_state_dispatcher_event.add_listener(listener)
