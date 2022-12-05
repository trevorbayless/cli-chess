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

from cli_chess.modules.token_manager import TokenManagerModel
from cli_chess.utils.config import LichessSection
from berserk.exceptions import BerserkError
from berserk import clients
from os import remove
import pytest


@pytest.fixture
def model(monkeypatch, lichess_config):
    monkeypatch.setattr('cli_chess.modules.token_manager.token_manager_model.lichess_config', lichess_config)
    return TokenManagerModel()


@pytest.fixture
def lichess_config():
    lichess_config = LichessSection("unit_test_config.ini")
    yield lichess_config
    remove(lichess_config.full_filename)


def test_is_lichess_token_valid(model: TokenManagerModel, lichess_config: LichessSection, monkeypatch):
    def mock_fail_get(*args, **kwargs):
        raise BerserkError

    def mock_success_get(*args, **kwargs):
        return {'username': 'mockuser'}

    # Test a mocked invalid lichess api token
    monkeypatch.setattr(clients.Account, "get", mock_fail_get)
    assert not model.is_lichess_token_valid("Abc123", save=True)
    assert lichess_config.get_value(LichessSection.Keys.API_TOKEN) == ""
    assert lichess_config.get_value(LichessSection.Keys.USERNAME) == ""

    # Test a mocked valid lichess api token
    monkeypatch.setattr(clients.Account, "get", mock_success_get)
    assert model.is_lichess_token_valid("Def456", save=False)
    assert lichess_config.get_value(LichessSection.Keys.API_TOKEN) == ""
    assert lichess_config.get_value(LichessSection.Keys.USERNAME) == ""

    # Test saving a mocked valid api token
    assert model.is_lichess_token_valid("Def456", save=True)
    assert lichess_config.get_value(LichessSection.Keys.API_TOKEN) == "Def456"
    assert lichess_config.get_value(LichessSection.Keys.USERNAME) == "mockuser"


def test_save_lichess_user(lichess_config: LichessSection):
    assert lichess_config.get_value(LichessSection.Keys.API_TOKEN) == ""
    assert lichess_config.get_value(LichessSection.Keys.USERNAME) == ""
    lichess_config.set_value(LichessSection.Keys.API_TOKEN, "  AbC123  ")
    lichess_config.set_value(LichessSection.Keys.USERNAME, "TestUser")
    assert lichess_config.get_value(LichessSection.Keys.API_TOKEN) == "AbC123"
    assert lichess_config.get_value(LichessSection.Keys.USERNAME) == "TestUser"


def test_get_lichess_username(lichess_config: LichessSection):
    assert lichess_config.get_value(LichessSection.Keys.USERNAME) == ""
    lichess_config.set_value(LichessSection.Keys.USERNAME, "testuser  ")
    assert lichess_config.get_value(LichessSection.Keys.USERNAME) == "testuser"
