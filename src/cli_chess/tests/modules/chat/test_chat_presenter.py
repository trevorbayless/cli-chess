from cli_chess.modules.chat import ChatModel, ChatPresenter
from unittest.mock import Mock, patch
import pytest


@pytest.fixture
def model():
    return ChatModel()


@pytest.fixture
def presenter(model: ChatModel):
    with patch("cli_chess.modules.chat.chat_presenter.ChatView") as MockView:
        MockView.return_value = Mock()
        p = ChatPresenter(model)
    return p


def test_init(model: ChatModel, presenter: ChatPresenter):
    assert presenter.update in model._event_listeners
    assert presenter.view is not None


def test_update_calls_view(model: ChatModel, presenter: ChatPresenter):
    presenter.view.update = Mock()

    model.add_message("alice", "hello")
    presenter.view.update.assert_called_once_with(model.get_messages())


def test_update_passes_all_messages(model: ChatModel, presenter: ChatPresenter):
    presenter.view.update = Mock()

    model.add_message("alice", "first")
    model.add_message("bob", "second")

    last_call_args = presenter.view.update.call_args[0][0]
    assert last_call_args == [
        {"username": "alice", "text": "first"},
        {"username": "bob", "text": "second"},
    ]


def test_update_without_messages(model: ChatModel, presenter: ChatPresenter):
    presenter.view.update = Mock()

    presenter.update()
    presenter.view.update.assert_called_once_with([])
