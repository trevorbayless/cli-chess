from cli_chess.core.game import PlayableGameModelBase
from cli_chess.core.game.game_options import GameOption
from cli_chess.core.api import GameStateDispatcher
from cli_chess.utils import log, threaded, RequestSuccessfullySent, EventTopics
from chess import COLORS, COLOR_NAMES, WHITE, BLACK, Color
from enum import Enum, auto
from typing import Optional, Dict


class EventSender(Enum):
    LOCAL = auto()
    FROM_IEM = auto()
    FROM_GSD = auto()


class OnlineGameModel(PlayableGameModelBase):
    """This model must only be used for games owned by the linked lichess user.
       Games not owned by this account must directly use the base model instead.
    """
    def __init__(self, game_parameters: dict, is_vs_ai: bool):
        super().__init__(play_as_color=game_parameters[GameOption.COLOR], variant=game_parameters[GameOption.VARIANT], fen=None)
        self.vs_ai = is_vs_ai
        self.playing_game_id = None
        self.searching = False
        self._update_game_metadata(EventTopics.GAME_PARAMS, sender=EventSender.LOCAL, data=game_parameters)
        self.game_state_dispatcher = Optional[GameStateDispatcher]

        try:
            from cli_chess.core.api.api_manager import api_client, api_iem
            self.api_iem = api_iem
            self.api_client = api_client
        except ImportError:
            # TODO: Clean this up so the error is displayed on the main screen
            log.error("Failed to import api_iem and api_client")
            raise ImportError("API client not setup. Do you have an API token linked?")

    @threaded
    def create_game(self) -> None:
        """Sends a request to lichess to start an AI challenge using the selected game parameters"""
        # Note: Only subscribe to IEM events right before creating challenge to lessen chance of grabbing another game
        self.api_iem.subscribe_to_events(self._handle_iem_event)
        self._notify_game_model_updated(EventTopics.GAME_SEARCH)
        self.searching = True

        if self.vs_ai:  # Challenge Lichess AI (stockfish)
            self.api_client.challenges.create_ai(level=self.game_metadata.players[not self.my_color].ai_level,
                                                 clock_limit=self.game_metadata.clocks[WHITE].time * 60,  # challenges need time in seconds
                                                 clock_increment=self.game_metadata.clocks[WHITE].increment,
                                                 color=COLOR_NAMES[self.game_metadata.my_color],
                                                 variant=self.game_metadata.variant)
        else:  # Find a random opponent
            self.api_client.board.seek(time=self.game_metadata.clocks[WHITE].time,
                                       increment=self.game_metadata.clocks[WHITE].increment,
                                       color=COLOR_NAMES[self.game_metadata.my_color],
                                       variant=self.game_metadata.variant,
                                       rated=self.game_metadata.rated,
                                       rating_range=None)

    def _start_game(self, game_id: str) -> None:
        """Called when a game is started. Sets proper class variables
           and starts and registers game stream event callback
        """
        if game_id and not self.game_in_progress:
            self._notify_game_model_updated(EventTopics.GAME_START)
            self.game_in_progress = True
            self.searching = False
            self.playing_game_id = game_id

            self.game_state_dispatcher = GameStateDispatcher(game_id)
            self.game_state_dispatcher.subscribe_to_events(self._handle_gsd_event)
            self.game_state_dispatcher.start()

    def _game_end(self) -> None:
        """The game we are playing has ended. Handle cleaning up."""
        self.game_in_progress = False
        self.searching = False
        self.playing_game_id = None
        self.api_iem.unsubscribe_from_events(self._handle_iem_event)

    def make_move(self, move: str):
        """Sends the move to the board model for a validity check. If valid this
           function will pass the move over to the game state dispatcher to be sent
           Raises an exception on move or API errors.
        """
        if self.game_in_progress:
            try:
                if not move:
                    raise Warning("No move specified")

                if move == "0000":
                    raise Warning("Null moves are not supported in online games")

                move = self.board_model.verify_move(move.strip())
                self.game_state_dispatcher.make_move(move)
            except Exception:
                raise
        else:
            log.warning("Attempted to make a move in a game that's not in progress")
            if self.searching:
                raise Warning("Still searching for opponent")
            else:
                raise Warning("Game has already ended")

    def set_premove(self, move: str) -> None:
        """Sets the premove. Raises an exception on an invalid premove"""
        if self.game_in_progress and move and not self.is_my_turn():
            if move == "0000":
                raise Warning("Null moves are not supported in online games")
            self.premove_model.set_premove(move)

    def propose_takeback(self) -> None:
        """Notifies the game state dispatcher to propose a takeback"""
        if self.game_in_progress:
            try:
                if len(self.board_model.get_move_stack()) < 2:
                    raise Warning("Cannot send takeback with less than two moves")

                self.premove_model.clear_premove()
                self.game_state_dispatcher.send_takeback_request()

                if not self.vs_ai:
                    raise RequestSuccessfullySent("Takeback request sent")
            except Exception:
                raise
        else:
            log.warning("Attempted to propose a takeback in a game that's not in progress")
            if self.searching:
                raise Warning("Still searching for opponent")
            else:
                raise Warning("Game has already ended")

    def offer_draw(self) -> None:
        """Notifies the game state dispatcher to offer a draw"""
        if self.game_in_progress:
            if self.vs_ai:
                raise Warning("Lichess AI does not accept draw offers")

            try:
                self.game_state_dispatcher.send_draw_offer()
                raise RequestSuccessfullySent("Draw offer sent")
            except Exception:
                raise
        else:
            log.warning("Attempted to offer a draw to a game that's not in progress")
            if self.searching:
                raise Warning("Still searching for opponent")
            else:
                raise Warning("Game has already ended")

    def resign(self) -> None:
        """Notifies the game state dispatcher to resign the game"""
        if self.game_in_progress:
            try:
                self.game_state_dispatcher.resign()
            except Exception:
                raise
        else:
            log.warning("Attempted to resign a game that's not in progress")
            if self.searching:
                raise Warning("Still searching for opponent")
            else:
                raise Warning("Game has already ended")

    def _handle_iem_event(self, *args, data: Optional[Dict] = None) -> None:
        """Handles events received from the IncomingEventManager. NOTE: Events coming in
           are global to the account, therefore multiple game start/end events can come in based
           on how many games are being played. Updates to game_metadata should only happen for
           the game actively being played.
        """
        if not data:
            return
        try:
            if EventTopics.GAME_START in args:
                # TODO: There has to be a better way to ensure this is the right game...
                #  add some further specific clauses like color, time control, date, etc?
                if not self.game_in_progress and not data.get('hasMoved') and data.get('compat', {}).get('board'):
                    self._update_game_metadata(*args, sender=EventSender.FROM_IEM, data=data)
                    self._start_game(data.get('gameId'))

            elif EventTopics.GAME_END in args:
                if self.game_in_progress and self.playing_game_id == data.get('gameId'):
                    self._update_game_metadata(*args, sender=EventSender.FROM_IEM, data=data)
                    self._game_end()
        except Exception as e:
            log.error(f"Error handling IncomingEventManager event: {e}")
            raise

    def _handle_gsd_event(self, *args, data: Optional[Dict] = None) -> None:
        """Handles received from the GameStateDispatcher. Incoming events are
           specific to this game being played
        """
        if not data:
            return
        try:
            if EventTopics.GAME_START in args:
                self.board_model.reinitialize_board(variant=self.game_metadata.variant,
                                                    orientation=(self.my_color if self.board_model.get_variant_name() != "racingkings" else WHITE),
                                                    fen=data.get('initialFen', ""))
                self.board_model.make_moves_from_list(data.get('state', {}).get('moves', []).split())

            elif EventTopics.MOVE_MADE in args:
                # TODO: Take some time measurements to see how much of an impact this approach is
                # Resetting and replaying the moves guarantees the game between lichess
                # and our local board are in sync (eg. takebacks, moves played on website, etc)
                self.board_model.reset(notify=False)
                self.board_model.make_moves_from_list(data.get('moves', []).split())

                if self.is_my_turn():
                    premove = self.premove_model.pop_premove()
                    try:
                        if premove:
                            self.make_move(premove)
                    except Exception as e:
                        if isinstance(e, ValueError):
                            log.debug(f"The premove set was invalid in the new context, skipping: {e}")
                        else:
                            log.exception(e)

                if EventTopics.GAME_END in args:
                    self._report_game_over(status=data.get('status'), winner=data.get('winner', ""))

            self._update_game_metadata(*args, sender=EventSender.FROM_GSD, data=data)
        except Exception as e:
            log.error(f"Error handling GameStateDispatcher event: {e}")
            raise

    def _update_game_metadata(self, *args, sender: Optional[EventSender] = None, data: Optional[Dict] = None, **kwargs) -> None:
        """Parses and saves the data of the game being played. Events come from senders
           in differing formats, which is why they are separated
        """
        if not sender or not data:
            return
        try:
            if sender is EventSender.LOCAL:
                if EventTopics.GAME_PARAMS in args:  # This is the data that came from the menu selections
                    self.game_metadata.my_color = self.my_color
                    self.game_metadata.variant = data.get(GameOption.VARIANT)
                    self.game_metadata.rated = data.get(GameOption.RATED, False)
                    self.game_metadata.players[not self.my_color].ai_level = data.get(GameOption.COMPUTER_SKILL_LEVEL) if self.vs_ai else None

                    for color in COLORS:
                        self.game_metadata.clocks[color].time = data.get(GameOption.TIME_CONTROL)[0]       # mins
                        self.game_metadata.clocks[color].increment = data.get(GameOption.TIME_CONTROL)[1]  # secs

            elif sender is EventSender.FROM_IEM:
                if EventTopics.GAME_START in args:
                    self.game_metadata.reset()
                    self.game_metadata.game_id = data.get('gameId')
                    self.game_metadata.my_color = self.my_color
                    self.game_metadata.rated = data.get('rated')
                    self.game_metadata.variant = data.get('variant', {}).get('name')
                    self.game_metadata.speed = data['speed']

                elif EventTopics.GAME_END in args:
                    self.game_metadata.players[self.my_color].rating_diff = data.get('ratingDiff', "")
                    self.game_metadata.players[not self.my_color].rating_diff = data.get('opponent', {}).get('ratingDiff', "")

            elif sender is EventSender.FROM_GSD:
                if EventTopics.GAME_START in args:
                    for color in COLOR_NAMES:
                        side_data = data.get(color, {})
                        color_as_bool = Color(COLOR_NAMES.index(color))
                        if side_data.get('name'):
                            self.game_metadata.players[color_as_bool].title = side_data.get('title')
                            self.game_metadata.players[color_as_bool].name = side_data.get('name', "?")
                            self.game_metadata.players[color_as_bool].rating = side_data.get('rating', "?")
                            self.game_metadata.players[color_as_bool].is_provisional_rating = side_data.get(
                                'provisional', False)
                        elif self.vs_ai:
                            self.game_metadata.players[
                                color_as_bool].name = f"Stockfish level {side_data.get('aiLevel', '?')}"

                        self.game_metadata.clocks[color_as_bool].units = "ms"
                        self.game_metadata.clocks[color_as_bool].time = data.get('state', {}).get(
                            'wtime' if color == "white" else 'btime')
                        self.game_metadata.clocks[color_as_bool].increment = data.get('state', {}).get(
                            'winc' if color == "white" else 'binc')

                elif EventTopics.MOVE_MADE in args:
                    self.game_metadata.clocks[WHITE].time = data.get('wtime')
                    self.game_metadata.clocks[BLACK].time = data.get('btime')

            self._notify_game_model_updated(*args, **kwargs)
        except Exception as e:
            log.exception(f"Error saving online game metadata: {e}")
            raise

    def _report_game_over(self, status: str, winner: str) -> None:
        """Saves game information and notifies listeners that the game has ended.
           This should only ever be called if the game is confirmed to be over
        """
        self._game_end()
        self.game_metadata.game_status.status = status  # status list can be found in lila status.ts
        self.game_metadata.game_status.winner = winner
        self._notify_game_model_updated(EventTopics.GAME_END)

    def cleanup(self) -> None:
        """Cleans up after this model by clearing event listeners and subscriptions.
           This should only ever be run when the models are no longer needed. This is
           called automatically on exit.
        """
        super().cleanup()

        if self.api_iem:
            self.api_iem.unsubscribe_from_events(self._handle_iem_event)
            log.debug(f"Cleared subscription from {type(self.api_iem).__name__} (id={id(self.api_iem)})")

        if self.game_in_progress:
            self.game_state_dispatcher.unsubscribe_from_events(self._handle_gsd_event)
            log.debug(f"Cleared subscription from {type(self.game_state_dispatcher).__name__} (id={id(self.game_state_dispatcher)})")
