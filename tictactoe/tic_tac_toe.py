#!/usr/bin/env python3
"""
Tic Tac Toe game.

Two-player console-based Tic Tac Toe game.
"""

def print_board(board):
    """
    Print the current board state.
    Board is a list of length 9.
    """
    print()
    for row in [board[i*3:(i+1)*3] for i in range(3)]:
        print('|'.join(f' {cell} ' for cell in row))
        if row != board[6:9]:
            print('-----------')
    print()

def check_win(board, player):
    """Check if the given player has won."""
    win_conditions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6),
    ]
    return any(board[a] == board[b] == board[c] == player for a, b, c in win_conditions)

def get_move(board, player):
    """Prompt the player for a move and validate input."""
    while True:
        try:
            choice = int(input(f"Player {player}, enter your move (1-9): ")) - 1
            if choice < 0 or choice > 8:
                print("Invalid cell. Choose a number from 1 to 9.")
            elif board[choice] != ' ':
                print("Cell already taken. Choose another one.")
            else:
                return choice
        except ValueError:
            print("Invalid input. Please enter a number from 1 to 9.")

def main():
    board = [' '] * 9
    current_player = 'X'
    for _ in range(9):
        print_board(board)
        move = get_move(board, current_player)
        board[move] = current_player
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break
        current_player = 'O' if current_player == 'X' else 'X'
    else:
        print_board(board)
        print("It's a draw!")

if __name__ == '__main__':
    main()