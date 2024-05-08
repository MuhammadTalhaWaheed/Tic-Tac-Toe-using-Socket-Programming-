import socket
import sys

class TicTacToeClient2:
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
            print(data)
            if "Player O's turn." in data:
                move = input("Enter your move (0-8): ")
                self.sock.sendall(move.encode())
            elif "That position is already taken" in data:
                move = input("Enter your move again (0-8): ")
                self.sock.sendall(move.encode())

if __name__ == "__main__":
    HOST = '127.0.0.1' 
    PORT = 65432       

    client2 = TicTacToeClient2(HOST, PORT)
    client2.connect()
