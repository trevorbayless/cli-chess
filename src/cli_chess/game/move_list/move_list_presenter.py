from . import MoveListView, MoveListModel

class MoveListPresenter:
    def __init__(self, model: MoveListModel):
        self.move_list_model = model
        self.move_list_view = MoveListView(self)


    def get_view(self):
        """Return the move list view"""
        return self.move_list_view


    def format_move_list(self) -> str:
        """Returns the formatted move list as a string"""
        output = ""
        move_list = self.move_list_model.get_san_move_list()
        for move in move_list:
            output += move

        return output


    def update_move_list(self):
        """Update the move list output"""
        self.move_list_view.update(self.format_move_list())
