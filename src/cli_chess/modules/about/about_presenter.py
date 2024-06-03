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
