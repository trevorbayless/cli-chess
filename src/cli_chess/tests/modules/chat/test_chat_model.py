from cli_chess.modules.chat import ChatModel
from unittest.mock import Mock
import pytest


@pytest.fixture
def listener():
    return Mock()


@pytest.fixture
def model(listener: Mock):
    m = ChatModel()
    m.add_event_listener(listener)
    return m


def test_init():
    m = ChatModel()
    assert m._messages == []
    assert m._event_listeners == []


def test_add_message(model: ChatModel, listener: Mock):
    model.add_message("alice", "hello")
    assert model._messages == [{"username": "alice", "text": "hello"}]
    listener.assert_called_once()

    listener.reset_mock()
    model.add_message("bob", "hi")
    assert len(model._messages) == 2
    assert model._messages[1] == {"username": "bob", "text": "hi"}
    listener.assert_called_once()


def test_get_messages(model: ChatModel):
    # Empty initially
    assert model.get_messages() == []

    model.add_message("alice", "hello")
    model.add_message("bob", "world")

    messages = model.get_messages()
    assert messages == [
        {"username": "alice", "text": "hello"},
        {"username": "bob", "text": "world"},
    ]

    messages.append({"username": "hacker", "text": "!"})
    assert len(model.get_messages()) == 2


def test_add_event_listener():
    m = ChatModel()
    cb1 = Mock()
    cb2 = Mock()

    m.add_event_listener(cb1)
    m.add_event_listener(cb2)
    assert cb1 in m._event_listeners
    assert cb2 in m._event_listeners


def test_notify_listeners(model: ChatModel, listener: Mock):
    listener.reset_mock()
    model._notify_listeners()
    listener.assert_called_once()

    second = Mock()
    model.add_event_listener(second)
    model._notify_listeners()
    listener.assert_called()
    second.assert_called_once()
