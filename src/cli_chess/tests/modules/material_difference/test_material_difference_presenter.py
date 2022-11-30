# Copyright (C) 2021-2022 Trevor Bayless <trevorbayless1@gmail.com>
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

from cli_chess.modules.material_difference import MaterialDifferenceModel, MaterialDifferencePresenter
from cli_chess.modules.board import BoardModel
from chess import WHITE, BLACK
from cli_chess.utils.config import BoardSection
from os import remove
import pytest


@pytest.fixture
def model():
    return MaterialDifferenceModel(BoardModel())


@pytest.fixture
def board_config():
    board_config = BoardSection("unit_test_config.ini")
    yield board_config
    remove(board_config.full_filename)


@pytest.fixture
def presenter(model: MaterialDifferenceModel, board_config: BoardSection, monkeypatch):
    monkeypatch.setattr('cli_chess.modules.material_difference.material_difference_presenter.board_config', board_config)
    return MaterialDifferencePresenter(model)


def test_update(model, presenter):
    # Todo: Still trying to determine best way to test. Just mock view calls?
    # Verify that update method is listening to model updates
    assert presenter.update in model.e_material_difference_model_updated.listeners


def test_format_diff_output(model: MaterialDifferenceModel, presenter: MaterialDifferencePresenter, board_config: BoardSection):
    assert presenter.format_diff_output(WHITE) == ""
    assert presenter.format_diff_output(BLACK) == ""

    # Test white advantage
    board_config.set_value(board_config.Keys.USE_UNICODE_PIECES, "yes")
    model.board_model.set_fen("1Q1B1K2/p3p3/p1PN4/p3q3/3N3k/pB6/P2r4/8 w - - 0 1")
    assert presenter.format_diff_output(WHITE) == "♝♝♞♞+4"
    assert presenter.format_diff_output(BLACK) == "♜♙♙♙"

    board_config.set_value(board_config.Keys.USE_UNICODE_PIECES, "no")
    assert presenter.format_diff_output(WHITE) == "BBNN+4"
    assert presenter.format_diff_output(BLACK) == "RPPP"

    # Test black advantage
    board_config.set_value(board_config.Keys.USE_UNICODE_PIECES, "yes")
    model.board_model.set_fen("3n4/1p4P1/1b1Kp3/1p1P2P1/1P1P2pk/1p6/pr6/8 w - - 0 1")
    assert presenter.format_diff_output(WHITE) == ""
    assert presenter.format_diff_output(BLACK) == "♜♝♞♙+12"

    board_config.set_value(board_config.Keys.USE_UNICODE_PIECES, "no")
    assert presenter.format_diff_output(WHITE) == ""
    assert presenter.format_diff_output(BLACK) == "RBNP+12"

    # Test no advantage
    board_config.set_value(board_config.Keys.USE_UNICODE_PIECES, "yes")
    model.board_model.set_fen("r1bqk2r/pppp1ppp/2n5/2b1p3/4P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4")
    assert presenter.format_diff_output(WHITE) == "♞"
    assert presenter.format_diff_output(BLACK) == "♝"

    board_config.set_value(board_config.Keys.USE_UNICODE_PIECES, "no")
    assert presenter.format_diff_output(WHITE) == "N"
    assert presenter.format_diff_output(BLACK) == "B"
