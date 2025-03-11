from tkinter import *
import random

def next_turn():
    pass

def check_winner():
    pass

def check_empty_spaces():
    pass

def new_game():
    pass

window = Tk()
window.title("Tic Tac Toe")
players = ['X', 'O']
player = random.choice(players)
buttons = [[0, 0, 0], 
           [0, 0, 0], 
           [0, 0, 0]]
label = Label(text=f"Player {player}'s turn")
label.pack(side=TOP)

reset_button = Button(text="restart", command=new_game)
reset_button.pack(side=TOP)

window.mainloop()