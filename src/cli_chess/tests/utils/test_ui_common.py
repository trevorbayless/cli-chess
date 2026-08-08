from cli_chess.utils.ui_common import NotationHelpContainer
from unittest.mock import patch


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
