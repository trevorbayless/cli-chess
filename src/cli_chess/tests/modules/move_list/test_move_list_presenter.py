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

from cli_chess.modules.move_list import MoveListModel, MoveListPresenter
from cli_chess.modules.board import BoardModel
from cli_chess.utils.config import BoardConfig
from os import remove
from unittest.mock import Mock
import pytest


@pytest.fixture
def model():
    return MoveListModel(BoardModel())


@pytest.fixture
def presenter(model: MoveListModel, board_config: BoardConfig, monkeypatch):
    monkeypatch.setattr('cli_chess.modules.move_list.move_list_presenter.board_config', board_config)
    return MoveListPresenter(model)


@pytest.fixture
def board_config():
    board_config = BoardConfig("unit_test_config.ini")
    yield board_config
    remove(board_config.full_filename)


def test_update(model: MoveListModel, presenter: MoveListPresenter, board_config: BoardConfig):
    # Verify the update method is listening to model updates
    assert presenter.update in model.e_move_list_model_updated.listeners

    # Verify the update method is listening to board configuration updates
    assert presenter.update in board_config.e_board_config_updated.listeners

    # Verify the presenter update function is calling the move list view
    # update function and passing in the formatted move data
    model.board_model.make_move("e4")
    presenter.view.update = Mock()
    presenter.update()
    move_data = presenter.get_formatted_move_list()
    presenter.view.update.assert_called_with(move_data)


def test_get_formatted_move_list(presenter: MoveListPresenter, board_config: BoardConfig):
    model = MoveListModel(BoardModel(fen="3pkb1r/P4pp1/8/8/8/8/1PPP3p/R2NKP2 w Qk - 0 40"))
    presenter.model = model

    # Test empty move list
    assert presenter.get_formatted_move_list() == []

    # Test unicode move list formatting
    board_config.set_value(board_config.Keys.USE_UNICODE_PIECES, "yes")
    moves = ["d4", "f5", "Nc3", "Bd6"]
    for move in moves:
        model.board_model.make_move(move)
    assert presenter.get_formatted_move_list() == ["d4", "f5", "♞c3", "♝d6"]

    # Test non-unicode move list formatting
    board_config.set_value(board_config.Keys.USE_UNICODE_PIECES, "no")
    assert presenter.get_formatted_move_list() == ["d4", "f5", "Nc3", "Bd6"]

    # Test move promotion formatting
    board_config.set_value(board_config.Keys.USE_UNICODE_PIECES, "yes")
    model.board_model.make_move("a8=N")
    model.board_model.make_move("h2h1Q")
    assert presenter.get_formatted_move_list() == ["d4", "f5", "♞c3", "♝d6", "a8=♞", "h1=♛"]

    # Test castling output
    model.board_model.make_move("e1c1")
    model.board_model.make_move("O-O")
    assert presenter.get_formatted_move_list() == ["d4", "f5", "♞c3", "♝d6", "a8=♞", "h1=♛", "O-O-O", "O-O"]

    # Test move list formatting when the first move is black
    board_config.set_value(board_config.Keys.USE_UNICODE_PIECES, "no")
    model = MoveListModel(BoardModel(fen="8/1PK5/8/8/8/8/4kp2/8 b - - 2 70"))
    presenter.model = model
    model.board_model.make_move("f1Q")
    assert presenter.get_formatted_move_list() == ["...", "f1=Q"]

    # Verify move list data is still produced on blindfold chess
    board_config.set_value(board_config.Keys.BLINDFOLD_CHESS, "yes")
    assert presenter.get_formatted_move_list() == ["...", "f1=Q"]


def test_get_move_as_unicode(presenter: MoveListPresenter, board_config: BoardConfig):
    board_config.set_value(board_config.Keys.USE_UNICODE_PIECES, "yes")
    model = MoveListModel(BoardModel(fen="r3kbn1/p2p3P/8/8/5p2/8/p3P3/RNBQK2R w KQq - 0 1"))
    presenter.model = model

    # Test pawn move
    model.board_model.make_move("e3")
    assert presenter.get_move_as_unicode(model.get_move_list_data()[-1]) == "e3"

    # Test pawn capture
    model.board_model.make_move("f4e3")
    assert presenter.get_move_as_unicode(model.get_move_list_data()[-1]) == "fxe3"

    # Test pawn promotion
    model.board_model.make_move("h8=N")
    assert presenter.get_move_as_unicode(model.get_move_list_data()[-1]) == "h8=♞"

    # Test pawn promotion with capture
    model.board_model.make_move("axb1R")
    assert presenter.get_move_as_unicode(model.get_move_list_data()[-1]) == "axb1=♜"

    # Test bishop move
    model.board_model.make_move("Bd2")
    assert presenter.get_move_as_unicode(model.get_move_list_data()[-1]) == "♝d2"

    # Test queenside castle
    model.board_model.make_move("O-O-O")
    assert presenter.get_move_as_unicode(model.get_move_list_data()[-1]) == "O-O-O"

    # Test kingside castle
    model.board_model.make_move("e1g1")
    assert presenter.get_move_as_unicode(model.get_move_list_data()[-1]) == "O-O"

    # Test null move
    model.board_model.make_move("0000")
    assert presenter.get_move_as_unicode(model.get_move_list_data()[-1]) == "--"
