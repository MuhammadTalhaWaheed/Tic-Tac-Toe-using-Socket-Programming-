import socket
import sys

class TicTacToeClient1:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.sock.connect((self.host, self.port))
            print("Connected to Tic Tac Toe server")
            self.play_game()
        except ConnectionRefusedError:
            print("Connection refused. Make sure the server is running.")
            sys.exit()

    def play_game(self):
        while True:
            data = self.sock.recv(1024).decode()
            if not data:
                break
            print("\n" + data)

            if "Player X's turn." in data:
                move = self.get_valid_move()
                if move.lower() == "exit":
                    self.sock.close()
                    sys.exit("You exited the game.")
                self.sock.sendall(move.encode())
            elif "That position is already taken" in data:
                move = self.get_valid_move()
                if move.lower() == "exit":
                    self.sock.close()
                    sys.exit("You exited the game.")
                self.sock.sendall(move.encode())
            elif "wins!" in data or "tie!" in data:
                print(self.sock.recv(1024).decode())
                break

    def get_valid_move(self):
        while True:
            move = input("Enter your move (0-8) or type 'exit' to quit: ")
            if move.lower() == "exit":
                exit()
            elif move.isdigit() and 0 <= int(move) <= 8:
                return move
            else:
                print("Invalid move. Please enter a number between 0 and 8.")
                move = input("or type 'exit' to quit: ")
                return move

if __name__ == "__main__":
    HOST = '127.0.0.1'  
    PORT = 65432        

    client1 = TicTacToeClient1(HOST, PORT)
    client1.connect()
