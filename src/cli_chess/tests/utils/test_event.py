from cli_chess.utils import Event, EventManager
from unittest.mock import Mock
import pytest


@pytest.fixture
def listener1():
    return Mock()


@pytest.fixture
def listener2():
    return Mock()


@pytest.fixture
def event(listener1):
    event = Event()
    event.add_listener(listener1)
    return event


@pytest.fixture
def event_manager():
    event_manger = EventManager()
    event_manger.create_event().add_listener(listener1)
    return event_manger


class TestEvent:
    def test_add_listener(self, event: Event, listener1: Mock, listener2: Mock):
        event.add_listener(listener2)
        assert listener2 in event.listeners

        event.add_listener(listener1)
        assert event.listeners.count(listener1) == 1

    def test_remove_listener(self, event: Event, listener1: Mock, listener2: Mock):
        assert listener2 not in event.listeners
        event.remove_listener(listener2)
        assert listener1 in event.listeners

        event.add_listener(listener2)
        event.remove_listener(listener1)
        assert listener1 not in event.listeners
        assert listener2 in event.listeners

    def test_notify(self, event: Event, listener1: Mock, listener2: Mock):
        listener1.assert_not_called()
        listener2.assert_not_called()

        event.notify()
        listener1.assert_called()
        listener2.assert_not_called()

        # Test notification after adding a listener
        listener1.reset_mock()
        event.add_listener(listener2)
        event.notify()
        listener1.assert_called()
        listener2.assert_called()

        # Test notification after removing a listener
        listener1.reset_mock()
        listener2.reset_mock()
        event.remove_listener(listener1)
        event.notify()
        listener1.assert_not_called()
        listener2.assert_called()

        # Try notifying without any listeners
        listener1.reset_mock()
        listener2.reset_mock()
        event.listeners.clear()
        assert not event.listeners
        event.notify()
        listener1.assert_not_called()
        listener2.assert_not_called()


class TestEventManager:
    def test_create_event(self, event_manager: EventManager, listener1: Mock):
        initial_len = len(event_manager._event_list)
        event = event_manager.create_event()
        event.add_listener(listener1)
        assert len(event_manager._event_list) - initial_len == 1
        assert isinstance(event_manager._event_list[-1], Event)

    def test_purge_all_event_listeners(self, event_manager: EventManager, listener2: Mock):
        event_manager.create_event().add_listener(listener2)
        assert len(event_manager._event_list) == 2

        # Verify events in the manager have listeners associated
        for event in event_manager._event_list:
            assert len(event.listeners) == 1

        # Purge listeners and verifying listeners are cleared but events still exist
        event_manager.purge_all_event_listeners()
        for event in event_manager._event_list:
            assert len(event.listeners) == 0
        assert len(event_manager._event_list) == 2

    def test_purge_all_events(self, event_manager: EventManager, listener2: Mock):
        """Purges all events in the event list by removing
           all associated events and listeners
        """
        test_event = event_manager.create_event()
        test_event.add_listener(listener2)
        assert len(event_manager._event_list) == 2

        # Test purging everything
        event_manager.purge_all_events()
        assert len(event_manager._event_list) == 0

        # Test firing a previously linked event
        test_event.notify()
        listener2.assert_not_called()
