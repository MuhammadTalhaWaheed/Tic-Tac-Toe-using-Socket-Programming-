import socket
import sys

class TicTacToeServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = []

    def start(self):
        print("Starting Tic Tac Toe server...")
        self.sock.bind((self.host, self.port))
        self.sock.listen(2)
        print("Server listening on {}:{}".format(self.host, self.port))

        while len(self.connections) < 2:
            conn, addr = self.sock.accept()
            self.connections.append(conn)
            print("Connected to client at", addr)

        print("Game started!")
        self.play_game()

    def send_to_all(self, msg):
        for conn in self.connections:
            conn.sendall(msg.encode())

    def play_game(self):
        board = [' ' for _ in range(9)]
        current_player = 'X'

        while True:
            self.send_to_all(self.print_board(board))

            player_move = self.get_player_move(current_player)

            if board[player_move] == ' ':
                board[player_move] = current_player
                if self.check_winner(board, current_player):
                    self.send_to_all(f"Player {current_player} wins!\n")
                    break
                if ' ' not in board:
                    self.send_to_all("It's a tie!\n")
                    break
                current_player = 'O' if current_player == 'X' else 'X'
            else:
                self.send_to_all("That position is already taken!\n")

        for conn in self.connections:
            conn.close()
        self.sock.close()

    def get_player_move(self, player):
        while True:
            self.send_to_all(f"Player {player}'s turn. Enter your move (0-8): ")
            move = int(self.connections[0].recv(1024).decode())
            if 0 <= move < 9:
                return move

    def print_board(self, board):
        rows = [" | ".join(board[i:i+3]) for i in range(0, 9, 3)]
        separator = "\n" + "-" * 9 + "\n"
        return separator.join(rows)
    def check_winner(self, board, player):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for condition in win_conditions:
            if all(board[i] == player for i in condition):
                return True
        return False


if __name__ == "__main__":
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

    server = TicTacToeServer(HOST, PORT)
    server.start()
