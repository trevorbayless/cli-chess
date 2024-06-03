from __future__ import annotations
from cli_chess.core.main.main_view import MainView
from cli_chess.menus.main_menu import MainMenuModel, MainMenuPresenter
from cli_chess.core.api.api_manager import required_token_scopes
from cli_chess.modules.token_manager.token_manager_model import g_token_manager_model
from cli_chess.utils import force_recreate_configs, print_program_config
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cli_chess.core.main import MainModel


class MainPresenter:
    def __init__(self, model: MainModel):
        self.model = model
        self._handle_startup_args()
        self.main_menu_presenter = MainMenuPresenter(MainMenuModel())
        self.view = MainView(self)

    def _handle_startup_args(self):
        """Handles the arguments passed"""
        args = self.model.startup_args

        if args.print_config:
            print_program_config()
            exit(0)

        if args.reset_config:
            force_recreate_configs()
            print("Configuration successfully reset")
            exit(0)

        if args.base_url:
            g_token_manager_model.set_base_url(args.base_url)

        if args.token:
            if not g_token_manager_model.update_linked_account(args.token):
                print(f"Invalid API token or missing required scopes. Scopes required: {required_token_scopes}")
                exit(1)

    def run(self):
        """Starts the main application"""
        self.view.run()
