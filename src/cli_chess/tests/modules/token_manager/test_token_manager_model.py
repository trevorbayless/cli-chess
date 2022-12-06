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
from cli_chess.utils.config import LichessConfig
from berserk.exceptions import BerserkError
from berserk import clients
from os import remove
from unittest.mock import Mock
import pytest


@pytest.fixture
def model_listener():
    return Mock()


@pytest.fixture
def model(model_listener: Mock, lichess_config: LichessConfig, monkeypatch):
    monkeypatch.setattr('cli_chess.modules.token_manager.token_manager_model.lichess_config', lichess_config)
    model = TokenManagerModel()
    model.e_token_manager_model_updated.add_listener(model_listener)
    return model


@pytest.fixture
def lichess_config():
    lichess_config = LichessConfig("unit_test_config.ini")
    yield lichess_config
    remove(lichess_config.full_filename)


def test_is_lichess_token_valid(model: TokenManagerModel, lichess_config: LichessConfig, monkeypatch):
    def mock_fail_get(*args, **kwargs):
        raise BerserkError

    def mock_success_get(*args, **kwargs):
        return {'username': 'mockuser'}

    # Test a mocked invalid lichess api token
    monkeypatch.setattr(clients.Account, "get", mock_fail_get)
    assert not model.is_lichess_token_valid("Abc123", save=True)
    assert lichess_config.get_value(LichessConfig.Keys.API_TOKEN) == ""
    assert lichess_config.get_value(LichessConfig.Keys.USERNAME) == ""

    # Test a mocked valid lichess api token
    monkeypatch.setattr(clients.Account, "get", mock_success_get)
    assert model.is_lichess_token_valid("Def456", save=False)
    assert lichess_config.get_value(LichessConfig.Keys.API_TOKEN) == ""
    assert lichess_config.get_value(LichessConfig.Keys.USERNAME) == ""

    # Test saving a mocked valid api token
    assert model.is_lichess_token_valid("Def456", save=True)
    assert lichess_config.get_value(LichessConfig.Keys.API_TOKEN) == "Def456"
    assert lichess_config.get_value(LichessConfig.Keys.USERNAME) == "mockuser"


def test_save_lichess_user(model: TokenManagerModel, lichess_config: LichessConfig, model_listener: Mock):
    assert lichess_config.get_value(LichessConfig.Keys.API_TOKEN) == ""
    assert lichess_config.get_value(LichessConfig.Keys.USERNAME) == ""
    model_listener.assert_not_called()

    model.save_lichess_user(api_token="  AbC123  ", username="TestUser")
    assert lichess_config.get_value(LichessConfig.Keys.API_TOKEN) == "AbC123"
    assert lichess_config.get_value(LichessConfig.Keys.USERNAME) == "TestUser"
    model_listener.assert_called()


def test_get_lichess_username(model: TokenManagerModel, lichess_config: LichessConfig):
    assert lichess_config.get_value(LichessConfig.Keys.USERNAME) == ""
    assert model.get_lichess_username() == ""

    lichess_config.set_value(LichessConfig.Keys.USERNAME, "testuser  ")
    assert model.get_lichess_username() == "testuser"


def test_notify_token_manager_model_updated(model: TokenManagerModel, model_listener: Mock):
    # Test registered successful move listener is called
    model._notify_token_manager_model_updated()
    model_listener.assert_called()

    # Unregister listener and test it's not called
    model_listener.reset_mock()
    model.e_token_manager_model_updated.remove_listener(model_listener)
    model._notify_token_manager_model_updated()
    model_listener.assert_not_called()
