# Tic-Tac-Toe-using-Socket-Programming-
This project implements a simple Tic Tac Toe game where two players can play against each other or against an AI opponent.

1. Features:
Player vs. Player mode: Two human players can play against each other.
Player vs. AI mode: A human player can play against an AI opponent.
AI opponent: Implements the minimax algorithm to make intelligent moves.
Socket-based multiplayer: Players can connect over a network to play against each other.

2. Usage
   
2.1 Server Setup:
Run the s.py script to start the server.
The server listens for incoming connections from players.

2.2 Client Setup:
Run the c1.py script to connect as Player 1 (X).
Run the c2.py script to connect as Player 2 (O) or play with the AI computer.
Follow the prompts to input moves and play the game.

Gameplay:
The game starts when both players are connected.
Each player takes turns making moves.
The game ends when one player wins, there's a tie, or a player exits the game.
