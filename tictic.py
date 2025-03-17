import tkinter as tk
from tkinter import messagebox, font
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("400x550")
        self.root.resizable(False, False)
        self.root.configure(bg="#2C3E50")
        
        # Game variables
        self.current_player = "X"
        self.board = [""] * 9
        self.game_over = False
        self.player_score = 0
        self.computer_score = 0
        self.tie_score = 0
        
        # Colors
        self.bg_color = "#2C3E50"
        self.title_color = "#ECF0F1"
        self.btn_color = "#3498DB"
        self.x_color = "#E74C3C"
        self.o_color = "#2ECC71"
        
        # Fonts
        self.title_font = font.Font(family="Helvetica", size=22, weight="bold")
        self.score_font = font.Font(family="Helvetica", size=12)
        self.button_font = font.Font(family="Helvetica", size=20, weight="bold")
        
        # Create GUI elements
        self.create_title_frame()
        self.create_score_frame()
        self.create_game_board()
        self.create_control_buttons()
    
    def create_title_frame(self):
        """Create the title frame with the game name"""
        title_frame = tk.Frame(self.root, bg=self.bg_color)
        title_frame.pack(pady=(20, 10))
        
        title_label = tk.Label(
            title_frame,
            text="Tic Tac Toe",
            font=self.title_font,
            bg=self.bg_color,
            fg=self.title_color
        )
        title_label.pack()
    
    def create_score_frame(self):
        """Create the score frame with player and computer scores"""
        self.score_frame = tk.Frame(self.root, bg=self.bg_color)
        self.score_frame.pack(pady=(0, 10))
        
        # Player score
        player_label = tk.Label(
            self.score_frame,
            text="You (X)",
            font=self.score_font,
            bg=self.bg_color,
            fg=self.x_color
        )
        player_label.grid(row=0, column=0, padx=20)
        
        self.player_score_label = tk.Label(
            self.score_frame,
            text="0",
            font=self.score_font,
            bg=self.bg_color,
            fg=self.x_color
        )
        self.player_score_label.grid(row=1, column=0)
        
        # Tie score
        tie_label = tk.Label(
            self.score_frame,
            text="Tie",
            font=self.score_font,
            bg=self.bg_color,
            fg=self.title_color
        )
        tie_label.grid(row=0, column=1, padx=20)
        
        self.tie_score_label = tk.Label(
            self.score_frame,
            text="0",
            font=self.score_font,
            bg=self.bg_color,
            fg=self.title_color
        )
        self.tie_score_label.grid(row=1, column=1)
        
        # Computer score
        computer_label = tk.Label(
            self.score_frame,
            text="Computer (O)",
            font=self.score_font,
            bg=self.bg_color,
            fg=self.o_color
        )
        computer_label.grid(row=0, column=2, padx=20)
        
        self.computer_score_label = tk.Label(
            self.score_frame,
            text="0",
            font=self.score_font,
            bg=self.bg_color,
            fg=self.o_color
        )
        self.computer_score_label.grid(row=1, column=2)
    
    def create_game_board(self):
        """Create the 3x3 game board"""
        self.game_frame = tk.Frame(
            self.root,
            bg=self.bg_color,
            width=312,
            height=312
        )
        self.game_frame.pack(pady=10)
        
        # Create 3x3 grid of buttons
        self.buttons = []
        for i in range(3):
            for j in range(3):
                btn = tk.Button(
                    self.game_frame,
                    text="",
                    font=self.button_font,
                    width=3,
                    height=1,
                    bg=self.btn_color,
                    command=lambda row=i, col=j: self.make_move(row, col)
                )
                btn.grid(row=i, column=j, padx=5, pady=5)
                self.buttons.append(btn)
    
    def create_control_buttons(self):
        """Create control buttons (New Game, Exit)"""
        control_frame = tk.Frame(self.root, bg=self.bg_color)
        control_frame.pack(pady=20)
        
        new_game_button = tk.Button(
            control_frame,
            text="New Game",
            font=self.score_font,
            bg="#F39C12",
            fg="white",
            width=10,
            command=self.reset_game
        )
        new_game_button.grid(row=0, column=0, padx=10)
        
        exit_button = tk.Button(
            control_frame,
            text="Exit",
            font=self.score_font,
            bg="#E74C3C",
            fg="white",
            width=10,
            command=self.root.quit
        )
        exit_button.grid(row=0, column=1, padx=10)
    
    def make_move(self, row, col):
        """Handle player's move and computer's response"""
        if self.game_over:
            return
        
        index = row * 3 + col
        if self.board[index] == "":
            # Player's move
            self.board[index] = "X"
            self.buttons[index].config(text="X", fg=self.x_color)
            
            # Check if player won
            if self.check_winner("X"):
                self.game_over = True
                self.player_score += 1
                self.player_score_label.config(text=str(self.player_score))
                messagebox.showinfo("Game Over", "You win!")
                return
            
            # Check for tie
            if "" not in self.board:
                self.game_over = True
                self.tie_score += 1
                self.tie_score_label.config(text=str(self.tie_score))
                messagebox.showinfo("Game Over", "It's a tie!")
                return
            
            # Computer's move
            self.root.after(300, self.computer_move)
    
    def computer_move(self):
        """Make computer's move"""
        if self.game_over:
            return
        
        # Try to make a winning move first
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "O"
                if self.check_winner("O"):
                    self.buttons[i].config(text="O", fg=self.o_color)
                    self.game_over = True
                    self.computer_score += 1
                    self.computer_score_label.config(text=str(self.computer_score))
                    messagebox.showinfo("Game Over", "Computer wins!")
                    return
                self.board[i] = ""
        
        # Try to block player's winning move
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "X"
                if self.check_winner("X"):
                    self.board[i] = "O"
                    self.buttons[i].config(text="O", fg=self.o_color)
                    return
                self.board[i] = ""
        
        # Take center if available
        if self.board[4] == "":
            self.board[4] = "O"
            self.buttons[4].config(text="O", fg=self.o_color)
            return
        
        # Take a corner if available
        corners = [0, 2, 6, 8]
        random.shuffle(corners)
        for i in corners:
            if self.board[i] == "":
                self.board[i] = "O"
                self.buttons[i].config(text="O", fg=self.o_color)
                return
        
        # Take any available space
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "O"
                self.buttons[i].config(text="O", fg=self.o_color)
                
                # Check if computer won
                if self.check_winner("O"):
                    self.game_over = True
                    self.computer_score += 1
                    self.computer_score_label.config(text=str(self.computer_score))
                    messagebox.showinfo("Game Over", "Computer wins!")
                return
    
    def check_winner(self, player):
        """Check if a player has won"""
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]               # Diagonals
        ]
        
        for combo in winning_combinations:
            if (self.board[combo[0]] == player and
                self.board[combo[1]] == player and
                self.board[combo[2]] == player):
                # Highlight winning combination
                for i in combo:
                    self.buttons[i].config(bg="#F39C12")
                return True
        return False
    
    def reset_game(self):
        """Reset the game board"""
        self.board = [""] * 9
        self.game_over = False
        
        for i in range(9):
            self.buttons[i].config(text="", bg=self.btn_color)

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
