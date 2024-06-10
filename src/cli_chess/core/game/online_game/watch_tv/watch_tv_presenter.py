from cli_chess.core.game import GamePresenterBase
from cli_chess.core.game.online_game.watch_tv import WatchTVModel, WatchTVView
from cli_chess.menus.tv_channel_menu import TVChannelMenuOptions
from cli_chess.utils.ui_common import change_views
from cli_chess.utils import AlertType, EventTopics


def start_watching_tv(channel: TVChannelMenuOptions) -> None:
    presenter = WatchTVPresenter(WatchTVModel(channel))
    change_views(presenter.view, presenter.view.move_list_placeholder) # noqa


class WatchTVPresenter(GamePresenterBase):
    def __init__(self, model: WatchTVModel):
        self.model = model
        super().__init__(model)

        self.model.start_watching()

    def _get_view(self) -> WatchTVView:
        """Sets and returns the view to use"""
        return WatchTVView(self)

    def update(self, *args, **kwargs) -> None:
        """Update method called on game model updates. Overrides base."""
        super().update(*args, **kwargs)
        if EventTopics.GAME_SEARCH in args:
            self.view.alert.show_alert("Searching for TV game...", AlertType.NEUTRAL)
        if EventTopics.ERROR in args:
            self.view.alert.show_alert(kwargs.get('msg', "An unspecified TV error has occurred"), AlertType.ERROR)

    def exit(self) -> None:
        """Stops TV and returns to the main menu"""
        self.model.stop_watching()
        self.view.exit()
