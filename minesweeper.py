# Copyright 2022, Tyler Brown

# This is a simple terminal-based version of Minesweeper.

# Minesweeper is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Minesweeper is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
# See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Minesweeper. If not, see <https://www.gnu.org/licenses/>.

import os
import sys
from random import *

##########
########## Class definitions
##########

class Cell:
    def __init__(self, stepped = False, bomb = False, flagged = False, question_mark = False, num_surrounding_bombs = 0, mask = " "):
        # becomes true when a player steps in that cell
        self.stepped = stepped
        self.bomb = bomb
        self.flagged = flagged
        self.question_mark = question_mark
        self.num_surrounding_bombs = num_surrounding_bombs
        # mask = could be blank, a flag, a bomb, or a number 0-8
        self.mask = mask

    # __str__ calls __repr__ internally.
    def __str__(self):
        return "{}".format(str(self.mask))

    def user_has_stepped(self):
        self.stepped = True

    def make_into_bomb(self):
        self.bomb = True

    def user_has_flagged(self):
        self.flagged = True
        self.set_mask('F')

    def user_placed_question_mark(self):
        self.question_mark = True

    def set_num_surrounding_bombs(self, number):
        self.num_surrounding_bombs = number

    def set_mask(self, value):
        self.mask = value

##########
########## Helpful functions
##########

def create_board(length, width):
    board = []
    for i in range(length):
        board.append([])
    for i in range(length):
        for j in range(width):
            board[i].append(Cell(mask=' ')) # note: this makes the Cell look empty
    return board

def print_board(board):
    length = len(board)
    width = len(board[0])
    print()
    # print the line at the top
    for j in range(width):
        print("----", end = "")
    print("-", end = "")
    print()
    # print the rest of the board, row by row
    for i in range(length):
        for j in range(width):
            print("| {} ".format(board[i][j]), end = "")
        print("|", end = "")
        print()
        for j in range(width):
            print("----", end = "")
        print("-", end = "")
        print()

def create_bombs(board):
    length = len(board)
    width = len(board[0])
    bomb_chance = 0.3
    for i in range(length):
        for j in range(width):
            #generate random number between 0 and 1
            if random() <= bomb_chance:
                board[i][j].bomb = True
    # print("Bombs have been created")

def number_the_board(board):
    length = len(board)
    width = len(board[0])
    for i in range(length):
        for j in range(width):
            if board[i][j].bomb == True:
                pass
            else: # see how many bombs are surrounding that cell, and set the number of surrounding bombs appropriately.
                board[i][j].num_surrounding_bombs = check_surrounding_cells(board, i, j)

def check_surrounding_cells(board, i, j):
    num_surrounding_bombs = 0
    length = len(board)
    width = len(board[0])
    # if cell is in the upper left corner
    if i == 0 and j == 0:
        if board[i+1][j].bomb is True:
            num_surrounding_bombs += 1
        if board[i+1][j+1].bomb is True:
            num_surrounding_bombs += 1
        if board[i][j+1].bomb is True:
            num_surrounding_bombs += 1
    elif i == 0 and j == width - 1:
        if board[i][j-1].bomb is True:
            num_surrounding_bombs += 1
        if board[i+1][j-1].bomb is True:
            num_surrounding_bombs += 1
        if board[i+1][j].bomb is True:
            num_surrounding_bombs += 1
    elif i == length - 1 and j == 0:
        if board[i-1][j].bomb is True:
            num_surrounding_bombs += 1
        if board[i-1][j+1].bomb is True:
            num_surrounding_bombs += 1
        if board[i][j+1].bomb is True:
            num_surrounding_bombs += 1
    elif i == length - 1 and j == width - 1:
        if board[i][j-1].bomb is True:
            num_surrounding_bombs += 1
        if board[i-1][j-1].bomb is True:
            num_surrounding_bombs += 1
        if board[i-1][j].bomb is True:
            num_surrounding_bombs += 1
    elif i == 0 and j > 0 and j < width - 1:
        if board[i][j-1].bomb is True:
            num_surrounding_bombs += 1
        if board[i+1][j-1].bomb is True:
            num_surrounding_bombs += 1
        if board[i+1][j].bomb is True:
            num_surrounding_bombs += 1
        if board[i+1][j+1].bomb is True:
            num_surrounding_bombs += 1
        if board[i][j+1].bomb is True:
            num_surrounding_bombs += 1
    elif i == length - 1 and j > 0 and j < width - 1:
        if board[i][j-1].bomb is True:
            num_surrounding_bombs += 1
        if board[i-1][j-1].bomb is True:
            num_surrounding_bombs += 1
        if board[i-1][j].bomb is True:
            num_surrounding_bombs += 1
        if board[i-1][j+1].bomb is True:
            num_surrounding_bombs += 1
        if board[i][j+1].bomb is True:
            num_surrounding_bombs += 1
    elif i > 0 and i < length - 1 and j == 0:
        if board[i-1][j].bomb is True:
            num_surrounding_bombs += 1
        if board[i-1][j+1].bomb is True:
            num_surrounding_bombs += 1
        if board[i][j+1].bomb is True:
            num_surrounding_bombs += 1
        if board[i+1][j+1].bomb is True:
            num_surrounding_bombs += 1
        if board[i+1][j].bomb is True:
            num_surrounding_bombs += 1
    elif i > 0 and i < length - 1 and j == width - 1:
        if board[i-1][j].bomb is True:
            num_surrounding_bombs += 1
        if board[i-1][j-1].bomb is True:
            num_surrounding_bombs += 1
        if board[i][j-1].bomb is True:
            num_surrounding_bombs += 1
        if board[i+1][j-1].bomb is True:
            num_surrounding_bombs += 1
        if board[i+1][j].bomb is True:
            num_surrounding_bombs += 1
    else:
        if board[i-1][j-1].bomb is True:
            num_surrounding_bombs += 1
        if board[i-1][j].bomb is True:
            num_surrounding_bombs += 1
        if board[i-1][j+1].bomb is True:    
            num_surrounding_bombs += 1
        if board[i][j-1].bomb is True:    
            num_surrounding_bombs += 1
        if board[i][j+1].bomb is True:    
            num_surrounding_bombs += 1
        if board[i+1][j-1].bomb is True:    
            num_surrounding_bombs += 1
        if board[i+1][j].bomb is True:    
            num_surrounding_bombs += 1
        if board[i+1][j+1].bomb is True:    
            num_surrounding_bombs += 1
    # print("cell is bomb = {}, row = {}, column = {}, bombs = {}".format(board[i][j].bomb, i, j, num_surrounding_bombs))
    return num_surrounding_bombs

# This function handles the stepping on a cell.
def step(game_board, row, column, dead):
    if (game_board[row][column].bomb == True):
        dead = True
    else:
        print("\nYou are not dead yet.")
    return dead

def reveal_all_bombs(board):
    length = len(board)
    width = len(board[0])
    for i in range(length):
        for j in range(width):    
            if board[i][j].bomb == True:
                board[i][j].set_mask('B')

##########
########## The main program
##########

print("\nMinesweeper, Copyright 2022, Tyler Brown")
print("\nThis program is free software, licensed under GNU GPL version 3.")

length = 10
width = 10
game_board = create_board(length, width)
create_bombs(game_board)
number_the_board(game_board)
print_board(game_board)

# keep going until the player is dead.
# at the start, the player is not dead.
dead = False
while (dead == False):
    action = ''
    while(action != 'f' and action != 's'):
        # ask whether player wants to flag or step
        action = input("\nWould you like to flag a cell, or take a step? ")
        if (action != ''):
            if (action != 'f' and action != 's'):
                print("\nYou must choose between setting a flag (f) or taking a step (s).")
            
    # ask for the ordered pair
    # print("\nTo choose the cell, supply a row and a column.")
    row = int(input("\nRow: "))
    column = int(input("\nColumn: "))

    if action == 'f':
        game_board[row][column].user_has_flagged()
    elif action == 's':
        dead = step(game_board, row, column, dead)
        if dead == False:
            num_surrounding_bombs_local = game_board[row][column].num_surrounding_bombs
            game_board[row][column].mask = num_surrounding_bombs_local
        else:
            game_board[row][column].mask = 'B'

    if dead == True:
        print("\nGame over, man! Game over!")
        reveal_all_bombs(game_board)
        print_board(game_board)
    else:
        print_board(game_board)


