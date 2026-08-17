from cli_chess.utils.ui_common import AlertContainer, NotationHelpContainer
from unittest.mock import patch


def test_append_alert_on_empty_label_shows_alert():
    with patch("cli_chess.utils.ui_common.repaint_ui"):
        alert = AlertContainer()
        alert.append_alert("Game saved: /tmp/game.pgn")

        assert alert._alert_label.text == "Game saved: /tmp/game.pgn"
        assert alert._alert_container.filter() is True


def test_append_alert_keeps_existing_text():
    with patch("cli_chess.utils.ui_common.repaint_ui"):
        alert = AlertContainer()
        alert.show_alert("Checkmate • White is victorious")
        alert.append_alert("Game saved: /tmp/game.pgn")

        assert alert._alert_label.text == "Checkmate • White is victorious\nGame saved: /tmp/game.pgn"


def test_notation_help_starts_hidden():
    with patch("cli_chess.utils.ui_common.repaint_ui"):
        nh = NotationHelpContainer()
    assert nh._visible is False


def test_notation_help_toggle_flips_visibility():
    with patch("cli_chess.utils.ui_common.repaint_ui"):
        nh = NotationHelpContainer()
        nh.toggle()
        assert nh._visible is True
        nh.toggle()
        assert nh._visible is False
