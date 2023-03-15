# Copyright (C) 2021-2023 Trevor Bayless <trevorbayless1@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from cli_chess.modules.about import AboutView
from cli_chess.utils.common import open_url_in_browser

CLI_CHESS_GITHUB_URL = "https://github.com/trevorbayless/cli-chess/"
CLI_CHESS_GITHUB_ISSUE_URL = CLI_CHESS_GITHUB_URL + "issues/new?assignees=&labels=bug&template=bug.yml"


class AboutPresenter:
    def __init__(self):
        self.view = AboutView(self)

    @staticmethod
    def open_github_url() -> None:
        """Open the cli-chess GitHub URL"""
        open_url_in_browser(CLI_CHESS_GITHUB_URL)

    @staticmethod
    def open_github_issue_url() -> None:
        """Opens the cli-chess GitHub issue URL"""
        open_url_in_browser(CLI_CHESS_GITHUB_ISSUE_URL)
