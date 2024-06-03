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


def mock_success_test_tokens(*args): # noqa
    return {
        'lip_validToken': {
            'scopes': 'board:play,challenge:read,challenge:write',
            'userId': 'testUser',
            'expires': None
        }
    }


def test_update(model: TokenManagerModel, presenter: TokenManagerPresenter, lichess_config: LichessConfig):
    # Verify this method is listening to model updates
    assert presenter.update in model.e_token_manager_model_updated.listeners
    model.save_account_data(api_token="lip_validToken", account_data=mock_success_test_tokens())
    assert presenter.view.lichess_username == model.linked_account
