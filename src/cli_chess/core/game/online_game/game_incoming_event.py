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

import threading


class GameIncomingEvent(threading.Thread):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.my_games = []
        self.my_challenge_queue = []

    def run(self) -> None:
        for event in self.client.board.stream_incoming_events():
            if event['type'] == 'gameStart':  # Start of a game
                self.my_games.append(event)

            elif event['type'] == 'gameFinish':  # Completion of a game
                if event in self.my_games:
                    self.my_games.remove(event)

            elif event['type'] == 'challenge':  # A challenge was sent by us or to us
                pass
                # When an initial challenge is created online, it's created as a "open" challenge.
                # Anyone that is given the URL can join that challenge. destUser == None
                # self.my_challenge_queue.append(event)
                # {'challenge': {'challenger': {'id': 'trevorbayless',
                #                               'name': 'trevorbayless',
                #                               'online': True,
                #                               'patron': True,
                #                               'rating': 1199,
                #                               'title': None},
                #                'color': 'white',
                #                'destUser': {'id': 'apitesting',
                #                             'name': 'apitesting',
                #                             'online': True,
                #                             'provisional': True,
                #                             'rating': 1500,
                #                             'title': None},
                #                'id': '1Jra1a2U',
                #                'perf': {'icon': '#', 'name': 'Rapid'},
                #                'rated': True,
                #                'speed': 'rapid',
                #                'status': 'created',
                #                'timeControl': {'increment': 8,
                #                                'limit': 840,
                #                                'show': '14+8',
                #                                'type': 'clock'},
                #                'url': 'https://lichess.org/1Jra1a2U',
                #                'variant': {'key': 'standard',
                #                            'name': 'Standard',
                #                            'short': 'Std'}},
                #  'type': 'challenge'}

            elif event['type'] == 'challengeCanceled':  # A challenge was cancelled
                pass
                # if event in self.my_challenge_queue:
                #     self.my_challenge_queue.remove(event)
                # {'challenge': {'challenger': {'id': 'trevorbayless',
                #                               'name': 'trevorbayless',
                #                               'online': True,
                #                               'patron': True,
                #                               'provisional': True,
                #                               'rating': 1500,
                #                               'title': None},
                #                'color': 'white',
                #                'destUser': {'id': 'apitesting',
                #                             'name': 'apitesting',
                #                             'online': True,
                #                             'provisional': True,
                #                             'rating': 1500,
                #                             'title': None},
                #                'id': 'ef0kBEFv',
                #                'perf': {'icon': '\ue00b', 'name': 'Crazyhouse'},
                #                'rated': False,
                #                'speed': 'correspondence',
                #                'status': 'created',
                #                'timeControl': {'type': 'unlimited'},
                #                'url': 'https://lichess.org/ef0kBEFv',
                #                'variant': {'key': 'crazyhouse',
                #                            'name': 'Crazyhouse',
                #                            'short': 'Crazy'}},
                #  'type': 'challengeCanceled'}

            elif event['type'] == 'challengeDeclined':  # A challenge was declined
                pass
                # {'challenge': {'challenger': {'id': 'trevorbayless',
                #                               'name': 'trevorbayless',
                #                               'online': True,
                #                               'patron': True,
                #                               'rating': 1199,
                #                               'title': None},
                #                'color': 'white',
                #                'declineReason': 'This is not the right time for me, please ask '
                #                                 'again later.',
                #                'destUser': {'id': 'apitesting',
                #                             'name': 'apitesting',
                #                             'online': True,
                #                             'provisional': True,
                #                             'rating': 1500,
                #                             'title': None},
                #                'id': '1Jra1a2U',
                #                'perf': {'icon': '#', 'name': 'Rapid'},
                #                'rated': True,
                #                'speed': 'rapid',
                #                'status': 'declined',
                #                'timeControl': {'increment': 8,
                #                                'limit': 840,
                #                                'show': '14+8',
                #                                'type': 'clock'},
                #                'url': 'https://lichess.org/1Jra1a2U',
                #                'variant': {'key': 'standard',
                #                            'name': 'Standard',
                #                            'short': 'Std'}},
                #  'type': 'challengeDeclined'}

    def get_active_games(self) -> list:
        """Returns a list of games in progress for this account"""
        return self.my_games

    def get_challenge_queue(self) -> list:
        """Returns a list of challenges sent to this account
           which are waiting for a response
        """
        return self.my_challenge_queue
