from __future__ import annotations
from cli_chess.modules.move_list import MoveListView
from cli_chess.modules.common import get_piece_unicode_symbol
from cli_chess.utils.config import game_config
from chess import BLACK, PAWN
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from cli_chess.modules.move_list import MoveListModel


class MoveListPresenter:
    def __init__(self, model: MoveListModel):
        self.model = model
        self.view = MoveListView(self)

        self.model.e_move_list_model_updated.add_listener(self.update)
        game_config.e_game_config_updated.add_listener(self.update)

    def update(self) -> None:
        """Update the move list output"""
        self.view.update(self.get_formatted_move_list())

    def get_formatted_move_list(self) -> List[str]:
        """Returns a list containing the formatted moves"""
        formatted_move_list = []
        move_list_data = self.model.get_move_list_data()
        use_unicode = game_config.get_boolean(game_config.Keys.SHOW_MOVE_LIST_IN_UNICODE)
        pad_unicode = game_config.get_boolean(game_config.Keys.PAD_UNICODE)

        for entry in move_list_data:
            move = self.get_move_as_unicode(entry, pad_unicode) if use_unicode else (entry['move'])

            if entry['turn'] == BLACK:
                if not formatted_move_list:  # The list starts with a move from black
                    formatted_move_list.append("...")

            formatted_move_list.append(move)
        return formatted_move_list

    @staticmethod
    def get_move_as_unicode(move_data: dict, pad_unicode=False) -> str:
        """Returns the passed in move data in unicode representation"""
        output = ""
        move = move_data.get('move')
        if move:
            output = move
            if move_data['piece_type'] and move_data['piece_type'] != PAWN and not move_data['is_castling']:
                piece_unicode_symbol = get_piece_unicode_symbol(move_data['piece_symbol'])

                if piece_unicode_symbol and pad_unicode:
                    # Pad unicode symbol with a space (if pad_unicode is true) to help unicode/ascii character overlap
                    piece_unicode_symbol = piece_unicode_symbol + " "

                output = piece_unicode_symbol + move[1:]

            if move_data['is_promotion']:
                eq_index = output.find("=")
                if eq_index != -1:
                    promotion_unicode_symbol = get_piece_unicode_symbol(output[eq_index+1])
                    output = output[:eq_index+1] + promotion_unicode_symbol + output[eq_index+2:]

        return output if output else move
