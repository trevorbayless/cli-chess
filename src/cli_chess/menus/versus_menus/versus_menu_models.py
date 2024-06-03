from cli_chess.menus import MultiValueMenuModel, MultiValueMenuOption, MenuCategory
from cli_chess.core.game.game_options import GameOption, OfflineGameOptions, OnlineGameOptions, OnlineDirectChallengesGameOptions


class VersusMenuModel(MultiValueMenuModel):
    def __init__(self, menu: MenuCategory):
        self.menu = menu
        super().__init__(self.menu)


class OfflineVsComputerMenuModel(VersusMenuModel):
    def __init__(self):
        self.menu = self._create_menu()
        super().__init__(self.menu)

    @staticmethod
    def _create_menu() -> MenuCategory:
        """Create the offline menu options"""
        menu_options = [
            MultiValueMenuOption(GameOption.VARIANT, "Choose the variant to play", [option for option in OfflineGameOptions.variant_options_dict]),  # noqa: E501
            MultiValueMenuOption(GameOption.SPECIFY_ELO, "Would you like the computer to play as a specific Elo?", ["No", "Yes"]),
            MultiValueMenuOption(GameOption.COMPUTER_SKILL_LEVEL, "Choose the skill level of the computer", [option for option in OfflineGameOptions.skill_level_options_dict]),  # noqa: E501
            MultiValueMenuOption(GameOption.COMPUTER_ELO, "Choose the Elo of the computer", list(range(500, 2850, 25)), visible=False),
            MultiValueMenuOption(GameOption.COLOR, "Choose the side you would like to play as", [option for option in OfflineGameOptions.color_options]),  # noqa: E501
        ]
        return MenuCategory("Play Offline vs Computer", menu_options)

    def show_elo_selection_option(self, show: bool):
        """Show/hide the Computer Elo option. Enabling the 'Specify Elo' selection
           Will disable the 'Computer SKill' Level option as only of these can be set
        """
        # Todo: Figure out a cleaner way so a loop isn't required
        for i, opt in enumerate(self.menu.category_options):
            if opt.option == GameOption.COMPUTER_ELO:
                opt.visible = show
            if opt.option == GameOption.COMPUTER_SKILL_LEVEL:
                opt.visible = not show


class OnlineVsComputerMenuModel(VersusMenuModel):
    def __init__(self):
        self.menu = self._create_menu()
        super().__init__(self.menu)

    @staticmethod
    def _create_menu() -> MenuCategory:
        """Create the online menu options"""
        menu_options = [
            MultiValueMenuOption(GameOption.VARIANT, "Choose the variant to play", [option for option in OnlineDirectChallengesGameOptions.variant_options_dict]),  # noqa: E501
            MultiValueMenuOption(GameOption.TIME_CONTROL, "Choose the time control", [option for option in OnlineDirectChallengesGameOptions.time_control_options_dict]),  # noqa: E501
            MultiValueMenuOption(GameOption.COMPUTER_SKILL_LEVEL, "Choose the skill level of the computer", [option for option in OnlineDirectChallengesGameOptions.skill_level_options_dict]),  # noqa: E501
            MultiValueMenuOption(GameOption.COLOR, "Choose the side you would like to play as", [option for option in OnlineDirectChallengesGameOptions.color_options]),  # noqa: E501
        ]
        return MenuCategory("Play Online vs Computer", menu_options)


class OnlineVsRandomOpponentMenuModel(VersusMenuModel):
    def __init__(self):
        self.menu = self._create_menu()
        super().__init__(self.menu)

    @staticmethod
    def _create_menu() -> MenuCategory:
        """Create the online menu options"""
        menu_options = [
            MultiValueMenuOption(GameOption.VARIANT, "Choose the variant to play", [option for option in OnlineGameOptions.variant_options_dict]),  # noqa: E501
            MultiValueMenuOption(GameOption.TIME_CONTROL, "Choose the time control", [option for option in OnlineGameOptions.time_control_options_dict]),  # noqa: E501
            MultiValueMenuOption(GameOption.RATED, "Choose if you'd like to play a casual or rated game", [option for option in OnlineGameOptions.rated_options_dict]),  # noqa: E501
            MultiValueMenuOption(GameOption.COLOR, "Choose the side you would like to play as", [option for option in OnlineGameOptions.color_options]),  # noqa: E501
        ]
        return MenuCategory("Play Online vs Random Opponent", menu_options)
