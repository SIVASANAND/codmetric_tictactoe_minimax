"""
Tic Tac Toe with Minimax AI (Tkinter GUI)

- Human = X
- AI = O
- AI uses minimax to always play optimally
"""

import tkinter as tk
import math

# Global variables
HUMAN = 'X'
AI = 'O'
EMPTY = ' '

board = [EMPTY] * 9
buttons = []

# ---------------- AI Logic ----------------
def is_winner(brd, player):
    win_combos = [
        [0,1,2], [3,4,5], [6,7,8],  # rows
        [0,3,6], [1,4,7], [2,5,8],  # cols
        [0,4,8], [2,4,6]            # diags
    ]
    return any(all(brd[i] == player for i in combo) for combo in win_combos)

def is_board_full(brd):
    return all(cell != EMPTY for cell in brd)

def get_available_moves(brd):
    return [i for i in range(9) if brd[i] == EMPTY]

def minimax(brd, depth, is_maximizing):
    if is_winner(brd, AI):
        return 1
    elif is_winner(brd, HUMAN):
        return -1
    elif is_board_full(brd):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for move in get_available_moves(brd):
            brd[move] = AI
            score = minimax(brd, depth + 1, False)
            brd[move] = EMPTY
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for move in get_available_moves(brd):
            brd[move] = HUMAN
            score = minimax(brd, depth + 1, True)
            brd[move] = EMPTY
            best_score = min(score, best_score)
        return best_score

def ai_move():
    best_score = -math.inf
    move = None
    for i in get_available_moves(board):
        board[i] = AI
        score = minimax(board, 0, False)
        board[i] = EMPTY
        if score > best_score:
            best_score = score
            move = i
    return move

# ---------------- Tkinter GUI ----------------
def on_click(index):
    if board[index] == EMPTY and not game_over():
        # Human move
        board[index] = HUMAN
        buttons[index].config(text=HUMAN, state="disabled")

        if check_game_state():
            return

        # AI move
        ai = ai_move()
        if ai is not None:
            board[ai] = AI
            buttons[ai].config(text=AI, state="disabled")
            check_game_state()

def check_game_state():
    if is_winner(board, HUMAN):
        status_label.config(text="Congratulations! You win 🎉", fg="blue")
        disable_all()
        return True
    elif is_winner(board, AI):
        status_label.config(text="AI wins! 🤖", fg="red")
        disable_all()
        return True
    elif is_board_full(board):
        status_label.config(text="It's a tie!", fg="green")
        disable_all()
        return True
    return False

def game_over():
    return is_winner(board, HUMAN) or is_winner(board, AI) or is_board_full(board)

def disable_all():
    for btn in buttons:
        btn.config(state="disabled")

def reset_game():
    global board
    board = [EMPTY] * 9
    for btn in buttons:
        btn.config(text="", state="normal")
    status_label.config(text="Your turn! You are X.", fg="black")

# ---------------- Main App ----------------
root = tk.Tk()
root.title("Tic Tac Toe (Minimax AI)")

status_label = tk.Label(root, text="Your turn! You are X.", font=("Arial", 14))
status_label.pack(pady=10)

frame = tk.Frame(root)
frame.pack()

for i in range(9):
    btn = tk.Button(frame, text="", width=8, height=4,
                    font=("Arial", 18),
                    command=lambda i=i: on_click(i))
    btn.grid(row=i//3, column=i%3)
    buttons.append(btn)

reset_btn = tk.Button(root, text="Reset Game", command=reset_game, font=("Arial", 12))
reset_btn.pack(pady=10)

root.mainloop()