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

from cli_chess.utils import Event
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


def test_add_listener(event, listener1, listener2):
    event.add_listener(listener2)
    assert listener2 in event.listeners

    event.add_listener(listener1)
    assert event.listeners.count(listener1) == 1


def test_remove_listener(event, listener1, listener2):
    assert listener2 not in event.listeners
    event.remove_listener(listener2)
    assert listener1 in event.listeners

    event.add_listener(listener2)
    event.remove_listener(listener1)
    assert listener1 not in event.listeners
    assert listener2 in event.listeners


def test_notify(event, listener1, listener2):
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
