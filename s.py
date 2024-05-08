import socket
import sys
import math

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
            for i, conn in enumerate(self.connections):
                self.send_to_all(self.print_board(board))
                if current_player == 'X' and i == 0:
                    conn.sendall("\nPlayer X's turn. ".encode())
                elif current_player == 'O' and i == 1:
                    conn.sendall("Player O's turn. ".encode())

                if current_player == 'X':
                    move = self.get_player_move(conn)
                else:
                    move = self.get_ai_move(board, 'O')

                if board[move] == ' ':
                    board[move] = current_player
                    if self.check_winner(board, current_player):
                        self.send_to_all(f"Player {current_player} wins!\n")
                        self.send_to_all(self.print_board(board))
                        return
                    if ' ' not in board:
                        self.send_to_all("It's a tie!\n")
                        self.send_to_all(self.print_board(board))
                        return
                    current_player = 'O' if current_player == 'X' else 'X'
                else:
                    conn.sendall("That position is already taken".encode())
                    move = self.get_player_move(conn)

            if ' ' not in board:
                break

        for conn in self.connections:
            conn.close()
        self.sock.close()

    def get_player_move(self, conn):
        while True:
            move = int(conn.recv(1024).decode())
            if 0 <= move < 9:
                return move

    def get_ai_move(self, board, player):
        best_score = -math.inf
        best_move = None
        for i in range(9):
            if board[i] == ' ':
                board[i] = player
                score = self.minimax(board, False)
                board[i] = ' '
                if score > best_score:
                    best_score = score
                    best_move = i
        return best_move

    def minimax(self, board, is_maximizing):
        if self.check_winner(board, 'X'):
            return -1
        elif self.check_winner(board, 'O'):
            return 1
        elif ' ' not in board:
            return 0

        if is_maximizing:
            best_score = -math.inf
            for i in range(9):
                if board[i] == ' ':
                    board[i] = 'O'
                    score = self.minimax(board, False)
                    board[i] = ' '
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for i in range(9):
                if board[i] == ' ':
                    board[i] = 'X'
                    score = self.minimax(board, True)
                    board[i] = ' '
                    best_score = min(score, best_score)
            return best_score

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
    HOST = '127.0.0.1' 
    PORT = 65432        
    server = TicTacToeServer(HOST, PORT)
    server.start()
