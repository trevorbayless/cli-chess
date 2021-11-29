from cli_chess.game.board import BoardModel
from chess import Move, Board, WHITE
from typing import List

class MoveListModel:
    def __init__(self, board_model: BoardModel) -> None:
        self.board_model = board_model

        # The board copy is used to generate the move list output
        # by using the move stack of the actual game on the board copy
        self.board_copy = BoardModel(variant=self.board_model.get_variant_name(),
                                     fen=self.board_model.get_initial_fen())


    def get_san_move_list(self) -> List[str]:
        """Returns the move list in standard notation"""
        san_move_list = []
        for move in self.board_model.get_move_stack():
            if not move:
                raise ValueError("Invalid move retrieved from move stack")

            if self.board_copy.board.turn == WHITE:
                san_move_list.append(f"{self.board_copy.board.san_and_push(move)}    ")
            elif not san_move_list:
                san_move_list.append(f"...{self.board_copy.board.san_and_push(move)}")
                san_move_list.append("\n")
            else:
                san_move_list.append(self.board_copy.board.san_and_push(move))
                san_move_list.append("\n")

        self.board_copy.board.reset()
        return san_move_list
