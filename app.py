from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

class TicTacToe:
    def __init__(self):
        self.board = [""] * 9
        self.current_player = "X"
        self.game_over = False
        self.winner = None
        self.tie = False

    def make_move(self, position):
        if self.board[position] == "" and not self.game_over:
            self.board[position] = self.current_player
            if self.check_winner():
                self.game_over = True
                self.winner = self.current_player
            elif "" not in self.board:
                self.game_over = True
                self.tie = True
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
            return True
        return False

    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]               # Diagonals
        ]
        
        for combo in winning_combinations:
            if (self.board[combo[0]] == self.current_player and
                self.board[combo[1]] == self.current_player and
                self.board[combo[2]] == self.current_player):
                return True
        return False

    def computer_move(self):
        if self.game_over:
            return None

        # Try to make a winning move
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "O"
                if self.check_winner():
                    self.game_over = True
                    self.winner = "O"
                    return i
                self.board[i] = ""

        # Try to block player's winning move
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "X"
                if self.check_winner():
                    self.board[i] = "O"
                    return i
                self.board[i] = ""

        # Take center if available
        if self.board[4] == "":
            self.board[4] = "O"
            return 4

        # Take a corner if available
        corners = [0, 2, 6, 8]
        random.shuffle(corners)
        for i in corners:
            if self.board[i] == "":
                self.board[i] = "O"
                return i

        # Take any available space
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "O"
                return i

        return None

game = TicTacToe()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/make_move', methods=['POST'])
def make_move():
    position = int(request.json.get('position'))
    if game.make_move(position):
        if not game.game_over:
            computer_position = game.computer_move()
            return jsonify({
                'board': game.board,
                'game_over': game.game_over,
                'winner': game.winner,
                'tie': game.tie,
                'computer_move': computer_position
            })
        return jsonify({
            'board': game.board,
            'game_over': game.game_over,
            'winner': game.winner,
            'tie': game.tie
        })
    return jsonify({'error': 'Invalid move'})

@app.route('/reset', methods=['POST'])
def reset_game():
    global game
    game = TicTacToe()
    return jsonify({'board': game.board})

if __name__ == '__main__':
    app.run(debug=True) 