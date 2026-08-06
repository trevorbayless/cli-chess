from cli_chess.core.game.game_options import GameOption, OnlineDirectChallengesGameOptions, OnlineVsComputerGameOptions


def test_direct_challenge_game_parameters():
    menu_selections = {
        GameOption.VARIANT: "King of the Hill",
        GameOption.TIME_CONTROL: "10+5 (Rapid)",
        GameOption.RATED: "Yes",
        GameOption.COLOR: "White",
    }
    assert OnlineDirectChallengesGameOptions().create_game_parameters_dict(menu_selections) == {
        GameOption.VARIANT: "kingOfTheHill",
        GameOption.TIME_CONTROL: (10, 5),
        GameOption.RATED: True,
        GameOption.COLOR: "white",
    }


def test_direct_challenge_casual_blitz_game_parameters():
    menu_selections = {
        GameOption.VARIANT: "Standard",
        GameOption.TIME_CONTROL: "3+0 (Blitz)",
        GameOption.RATED: "No",
        GameOption.COLOR: "Random",
    }
    assert OnlineDirectChallengesGameOptions().create_game_parameters_dict(menu_selections) == {
        GameOption.VARIANT: "standard",
        GameOption.TIME_CONTROL: (3, 0),
        GameOption.RATED: False,
        GameOption.COLOR: "random",
    }


def test_online_vs_computer_game_parameters():
    menu_selections = {
        GameOption.VARIANT: "Standard",
        GameOption.TIME_CONTROL: "5+3 (Blitz)",
        GameOption.COMPUTER_SKILL_LEVEL: "Level 3",
        GameOption.COLOR: "Black",
    }
    assert OnlineVsComputerGameOptions().create_game_parameters_dict(menu_selections) == {
        GameOption.VARIANT: "standard",
        GameOption.TIME_CONTROL: (5, 3),
        GameOption.COMPUTER_SKILL_LEVEL: 3,
        GameOption.COLOR: "black",
    }
