from __future__ import annotations
from prompt_toolkit.layout import Container, ConditionalContainer, VSplit, D, Window, FormattedTextControl, WindowAlign
from prompt_toolkit.widgets import Box
from prompt_toolkit.filters import Condition
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.modules.player_info import PlayerInfoPresenter
    from cli_chess.core.game import PlayerMetadata


class PlayerInfoView:
    def __init__(self, presenter: PlayerInfoPresenter, player_info: PlayerMetadata):
        self.presenter = presenter
        self.player_title = ""
        self.player_name = ""
        self.player_rating = ""
        self.rating_diff = ""
        self.update(player_info)

        self._player_title_control = FormattedTextControl(text=lambda: self.player_title, style="class:player-info.title")
        self._player_name_control = FormattedTextControl(text=lambda: self.player_name, style="class:player-info")
        self._player_rating_control = FormattedTextControl(text=lambda: self.player_rating, style="class:player-info")
        self._rating_diff_control = FormattedTextControl(text=lambda: self.rating_diff, style="class:player-info")
        self._container = self._create_container()

    def _create_container(self) -> Container:
        return VSplit([
            ConditionalContainer(
                Box(Window(self._player_title_control, align=WindowAlign.LEFT, dont_extend_width=True), padding=0, padding_right=1),
                Condition(lambda: False if not self.player_title else True)
            ),
            Box(Window(self._player_name_control, align=WindowAlign.LEFT, dont_extend_width=True), padding=0, padding_right=1),
            Box(Window(self._player_rating_control, align=WindowAlign.RIGHT, dont_extend_width=True), padding=0, padding_right=1),
            Box(Window(self._rating_diff_control, align=WindowAlign.RIGHT, dont_extend_width=True), padding=0, padding_right=1),

        ], width=D(min=1), height=D(max=1), window_too_small=ConditionalContainer(Window(), False))

    def update(self, player_info: PlayerMetadata) -> None:
        """Updates the player info using the data passed in"""
        self._set_player_title(player_info.title)
        self._set_player_name(player_info.name)
        self._set_player_rating(player_info.rating, player_info.is_provisional_rating)
        self._set_rating_diff(player_info.rating_diff)

    def _set_player_title(self, title: str):
        title = title if title else ""
        if title == "BOT":
            self._player_title_control.style = "class:player-info.title.bot"

        self.player_title = title

    def _set_player_name(self, name: str):
        self.player_name = name if name else ""

    def _set_player_rating(self, rating: str, provisional: bool):
        rating = rating if rating else ""
        self.player_rating = (f"({rating})" if not provisional else f"({rating}?)") if rating else ""

    def _set_rating_diff(self, rating_diff: int):
        """Handles formatting and updating the rating diff control"""
        if rating_diff:
            if rating_diff < 0:
                self._rating_diff_control.style = "class:player-info.neg-rating-diff"
                self.rating_diff = str(rating_diff)
            elif rating_diff > 0:
                self._rating_diff_control.style = "class:player-info.pos-rating-diff"
                self.rating_diff = "+" + str(rating_diff)
            else:
                self._rating_diff_control.style = "class:player-info"
                self.rating_diff = "+-0" + str()
        else:
            self.rating_diff = ""

    def __pt_container__(self) -> Container:
        """Returns this views container"""
        return self._container
