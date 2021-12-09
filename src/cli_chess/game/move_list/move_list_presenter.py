from . import MoveListView, MoveListModel
from cli_chess.game.common import get_piece_unicode_symbol
from cli_chess import config
from chess import WHITE, PAWN

class MoveListPresenter:
    def __init__(self, model: MoveListModel):
        self.move_list_model = model
        self.move_list_view = MoveListView(self)


    def get_view(self) -> MoveListView:
        """Return the move list view"""
        return self.move_list_view


    def format_move_list(self) -> str:
        """Returns the formatted move list as a string"""
        output = ""
        move_list_data = self.move_list_model.get_move_list_data()
        use_unicode = config.get_board_boolean(config.BoardKeys.USE_UNICODE_PIECES)

        for entry in move_list_data:
            turn = entry['turn']
            move = str(entry['move'])

            if use_unicode:
                move = self.get_move_as_unicode(entry)

            if turn == WHITE:
                output += move.ljust(8)
            elif not output:  # The list starts with a move from black
                output += "...".ljust(8)
                output += move
                output += "\n"
            else:
                output += move
                output += "\n"
        return output


    def get_move_as_unicode(self, move_data: dict) -> str:
        """Returns the passed in SAN move to unicode display"""
        output = ""
        move = move_data['move']
        if move:
            output = move
            if move_data['piece_type'] != PAWN:
                piece_unicode_symbol = get_piece_unicode_symbol(move_data['piece_symbol'])
                output = piece_unicode_symbol + move[1:]

            if move_data['promotion_symbol']:
                eq_index = output.find("=")
                if eq_index != -1:
                    promotion_unicode_symbol = get_piece_unicode_symbol(move_data['promotion_symbol'])
                    output = output[:eq_index+1] + promotion_unicode_symbol + output[eq_index+2:]

        if not output:
            output = move
        return output


    def update_move_list(self):
        """Update the move list output"""
        self.move_list_view.update(self.format_move_list())
