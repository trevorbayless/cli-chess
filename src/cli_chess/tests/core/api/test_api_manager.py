from cli_chess.modules.token_manager import token_manager_model
from cli_chess.core.api import api_manager


def test_api_token_has_scope(monkeypatch):
    monkeypatch.setattr(token_manager_model, "linked_token_scopes", {"board:play", "challenge:write"})
    assert api_manager.api_token_has_scope("challenge:write")
    assert not api_manager.api_token_has_scope("follow:read")

    monkeypatch.setattr(token_manager_model, "linked_token_scopes", set())
    assert not api_manager.api_token_has_scope("challenge:write")
