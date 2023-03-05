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


def mock_fail_test_tokens(*args): # noqa
    raise BerserkError


def mock_success_test_tokens(*args): # noqa
    return {
        'lip_validToken': {
            'scopes': 'board:play,challenge:read,challenge:write',
            'userId': 'testUser',
            'expires': None
        }
    }


def test_update_linked_account(model: TokenManagerModel, lichess_config: LichessConfig, model_listener: Mock, monkeypatch):
    # Test with empty api token
    assert not model.update_linked_account(api_token="")
    model_listener.assert_not_called()

    # Test a mocked invalid lichess api token and
    # verify existing user account data is not overwritten
    monkeypatch.setattr(clients.OAuth, "test_tokens", mock_fail_test_tokens)
    lichess_config.set_value(lichess_config.Keys.API_TOKEN, "lip_validToken")
    assert not model.update_linked_account(api_token="lip_badToken")
    assert lichess_config.get_value(lichess_config.Keys.API_TOKEN) == "lip_validToken"
    model_listener.assert_not_called()

    # Test a mocked valid lichess api token
    monkeypatch.setattr(clients.OAuth, "test_tokens", mock_success_test_tokens)
    lichess_config.set_value(lichess_config.Keys.API_TOKEN, "")
    assert model.update_linked_account(api_token="lip_validToken")
    assert lichess_config.get_value(lichess_config.Keys.API_TOKEN) == "lip_validToken"
    model_listener.assert_called()


def test_validate_token(model: TokenManagerModel, monkeypatch):
    # Test with empty API token
    assert model.validate_token(api_token="") is None

    # Test with invalid API token
    monkeypatch.setattr(clients.OAuth, "test_tokens", mock_fail_test_tokens)
    assert model.validate_token(api_token="lip_badToken") is None

    # Test with valid API token
    monkeypatch.setattr(clients.OAuth, "test_tokens", mock_success_test_tokens)
    assert model.validate_token(api_token="lip_validToken") == mock_success_test_tokens()['lip_validToken']


def test_save_account_data(model: TokenManagerModel, lichess_config: LichessConfig, model_listener: Mock):
    assert lichess_config.get_value(lichess_config.Keys.API_TOKEN) == ""
    model_listener.assert_not_called()

    model.save_account_data(api_token="  lip_validToken  ", account_data=mock_success_test_tokens())
    assert lichess_config.get_value(lichess_config.Keys.API_TOKEN) == "lip_validToken"
    model_listener.assert_called()


def test_notify_token_manager_model_updated(model: TokenManagerModel, model_listener: Mock):
    # Test registered successful move listener is called
    model._notify_token_manager_model_updated()
    model_listener.assert_called()

    # Unregister listener and test it's not called
    model_listener.reset_mock()
    model.e_token_manager_model_updated.remove_listener(model_listener)
    model._notify_token_manager_model_updated()
    model_listener.assert_not_called()
