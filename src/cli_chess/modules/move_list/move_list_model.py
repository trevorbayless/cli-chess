from cli_chess.modules.board import BoardModel
from cli_chess.utils import EventManager, log
from chess import piece_symbol
from typing import List


class MoveListModel:
    def __init__(self, board_model: BoardModel) -> None:
        self.board_model = board_model
        self.board_model.e_board_model_updated.add_listener(self.update)
        self.move_list_data = []

        self._event_manager = EventManager()
        self.e_move_list_model_updated = self._event_manager.create_event()
        self.update()

    def update(self, *args, **kwargs) -> None: # noqa
        """Updates the move list data using the latest move stack"""
        self.move_list_data.clear()

        # The move replay board is used to generate the move list output
        # by replaying the move stack of the actual game on the replay board
        move_replay_board = self.board_model.board.copy()
        move_replay_board.set_fen(self.board_model.initial_fen)

        for move in self.board_model.get_move_stack():
            piece_type = None
            if bool(move):
                piece_type = move_replay_board.piece_type_at(move.from_square) if not move.drop else move.drop

            try:
                san_move = move_replay_board.san(move)
                self.move_list_data.append({
                    'turn': move_replay_board.turn,
                    'move': san_move,
                    'piece_type': piece_type,
                    'piece_symbol': piece_symbol(piece_type) if bool(move) else None,
                    'is_castling': move_replay_board.is_castling(move),
                    'is_promotion': True if move.promotion else False,
                })
                move_replay_board.push_san(san_move)
            except ValueError as e:
                log.error(f"Error creating move list: {e}")
                log.error(f"Move list data: {self.board_model.get_move_stack()}")
                self.move_list_data.clear()
                break

        self._notify_move_list_model_updated()

    def get_move_list_data(self) -> List[dict]:
        """Returns the move list data"""
        return self.move_list_data

    def _notify_move_list_model_updated(self) -> None:
        """Notifies listeners of move list model updates"""
        self.e_move_list_model_updated.notify()

    def cleanup(self) -> None:
        """Handles model cleanup tasks. This should only ever
           be run when this model is no longer needed.
        """
        self._event_manager.purge_all_events()
