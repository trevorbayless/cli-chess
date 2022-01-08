from cli_chess.game.board import BoardModel
from cli_chess.utils import Event
from chess import Move, piece_symbol, WHITE, BLACK
from typing import List


class MoveListModel:
    def __init__(self, board_model: BoardModel) -> None:
        self.board_model = board_model
        self.board_model.e_board_model_updated.add_listener(self.update)

        # The move replay board is used to generate the move list output
        # by replaying the move stack of the actual game on the replay board
        self.move_replay_board = BoardModel(variant=self.board_model.get_variant_name(),
                                            fen=self.board_model.get_initial_fen())
        self.move_list_data = []

        self.e_move_list_model_updated = Event()
        self.update()


    def _move_list_model_updated(self) -> None:
        """Notifies listeners of move list model updates"""
        self.e_move_list_model_updated.notify()


    def update(self) -> None:
        """Updates the move list data using the latest move stack"""
        self.move_list_data.clear()
        self.move_replay_board.board.set_fen(self.board_model.get_initial_fen())

        for move in self.board_model.get_move_stack():
            if not move:
                raise ValueError(f"Invalid move ({move}) retrieved from move stack")

            color = WHITE if self.move_replay_board.board.turn == WHITE else BLACK

            # Use the drop piece type if this is a crazyhouse drop
            piece_type = self.move_replay_board.board.piece_type_at(move.from_square) if move.drop is None else move.drop
            symbol = piece_symbol(piece_type)
            is_castling = self.move_replay_board.board.is_castling(move)
            san_move = self.move_replay_board.board.san_and_push(move)

            move_data = {'turn': color,
                         'move': san_move,
                         'piece_type': piece_type,
                         'piece_symbol': symbol,
                         'is_castling': is_castling,
                         'is_promotion': True if move.promotion else False
            }

            self.move_list_data.append(move_data)

        self._move_list_model_updated()


    def get_move_list_data(self) -> List[dict]:
        """Returns the move list data"""
        return self.move_list_data
