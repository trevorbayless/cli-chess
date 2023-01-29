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

from cli_chess.modules.token_manager import TokenManagerModel, TokenManagerPresenter
from cli_chess.utils.config import LichessConfig
from os import remove
import pytest


@pytest.fixture
def model(monkeypatch, lichess_config):
    monkeypatch.setattr('cli_chess.modules.token_manager.token_manager_model.lichess_config', lichess_config)
    return TokenManagerModel()


@pytest.fixture
def presenter(model: TokenManagerModel):
    return TokenManagerPresenter(model)


@pytest.fixture
def lichess_config():
    lichess_config = LichessConfig("unit_test_config.ini")
    yield lichess_config
    remove(lichess_config.full_filename)


def test_update(model: TokenManagerModel, presenter: TokenManagerPresenter, lichess_config: LichessConfig):
    # Verify this method updates the view text
    lichess_config.set_value(lichess_config.Keys.USERNAME, "TestUsername")
    assert presenter.view.lichess_username == ""
    presenter.update()
    assert presenter.view.lichess_username == "TestUsername"

    # Verify this method is listening to model updates
    assert presenter.update in model.e_token_manager_model_updated.listeners
    model.save_account_data(api_token="ValidToken", username="TestUsername")
    assert presenter.view.lichess_username == "TestUsername"
