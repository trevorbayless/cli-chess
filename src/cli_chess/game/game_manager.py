import os
import threading
from pprint import pprint
from cli_chess.game import Board
from cli_chess import config
from cli_chess import common_utils
from prompt_toolkit import prompt

#Checkmate fen: 5rk1/5r2/8/8/8/8/8/6K1 b q - 0 1

def get_my_color(event):
    my_id = config.get_lichess_value(config.LichessKeys.USERNAME)
    my_color = "white"

    try:
        if my_id == event['black']['id']:
            my_color = "black"
    except Exception as e:
        print(e)

    return my_color


class GameManager(threading.Thread):
    def __init__(self, client, game_id):
        super().__init__()
        self.game_id = game_id
        self.client = client
        self.my_color = ""
        self.board = Board()
        self.moves = []


    def run(self):
        for event in self.client.board.stream_game_state(self.game_id):
            pprint(event)
            if event['type'] == 'gameFull':
                self.my_color = get_my_color(event)
                variant = event['variant']['name']
                fen = event['initialFen']

                if fen == "startpos":
                    fen = "" # allow the board to determine the start fen based on variant
                self.board = Board(self.my_color, variant, fen)
                self.handle_game_full(event)

            elif event['type'] == 'gameState':
                self.handle_state_change(event)

            elif event['type'] == 'chatLine':
                self.handle_chat_line(event)


    def handle_game_full(self, game_full):
        # print("\nGame full data:")
        # print("--------------------------")
        # pprint(game_full)
        # print("--------------------------\n")

        self.moves = game_full['state']['moves'].split()
        for move in self.moves:
            self.board.make_move(move)
        self.board.print_board()

        if self.is_my_turn():
            move = self.prompt_for_move()
            self.send_move_to_lichess(move)


    def handle_state_change(self, game_state):
        try:
            self.moves = game_state['moves'].split()
            last_move = self.moves[-1]
            self.board.make_move(last_move)
            #common_utils.clear_screen()
            self.board.print_board()
        except Exception as e:
            print(e)

        if self.board.is_game_over():
            print(self.board.game_result())

        elif self.is_my_turn():
            move = self.prompt_for_move()
            self.send_move_to_lichess(move)

        # print("\nGame state data:")
        # print("--------------------------")
        # pprint(game_state)
        # print("--------------------------\n")


    def handle_chat_line(self, chat_line):
        pass
        # print("\nGame chat data:")
        # print("--------------------------")
        # pprint(chat_line)
        # print("--------------------------\n")


    def prompt_for_move(self):
        """Prompts the user for a move and checks
           the legality before accepting. Returns
           the legal move.
        """
        #TODO: Handle promotion moves. Right now it will error on "a8", but not "a8q". Notify user of syntax.
        #TODO: Ability to show legal moves for a specific piece
        #TODO: Print message is move is too vague (eg. two knights can move to the same square)
        if not self.board.is_game_over():
            while(True):
                try:
                    if not self.board.is_game_over():
                        move = prompt("Your move: ")
                        move = self.board.parse_move(move)
                except ValueError as e:
                    print(e)
                    continue
                else:
                    return move


    def send_move_to_lichess(self, move):
        """Sends the passed in move to Lichess to make"""
        for i in range(10):
            try:
                self.client.board.make_move(self.game_id, move)
            except Exception as e:
                # Happend after asking for a takeback:
                   #HTTP 400: Bad Request: {'error': 'No piece on h2'}
                # Happened when a draw was claimed, but I entered a move in the prompt
                    #HTTP 400: Bad Request: {'error': 'Not your turn, or game already over'}

                print(e)
                print(f"({i}): An exception occurred sending the move to Lichess. Retrying.")
            else:
                break
        else:
            print("Unable to reconnect with Lichess. Please try restarting the program.")


    def is_my_turn(self):
        """Returns True if it is our turn"""
        return self.my_color == self.board.get_turn_color()