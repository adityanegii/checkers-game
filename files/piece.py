import pygame
from .constants import *


class Piece:
    '''Class representing checkers pieces'''

    OUTLINE = 2
    GAP = 10

    def __init__(self, row, col, color):
        '''Initialise a piece. Keep track of it's row/col, color, direction it goes, x/y position.'''
        self.row = row
        self.col = col
        self.color = color
        self.king = False

        self.available_moves = []
        self.capturing_moves = []

        if self.color == BLACK_PIECES:
            self.direction = 1
        else:
            self.direction = -1

        self.pos()

    def pos(self):
        '''Method to calculate the position of the piece'''
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def draw(self, win):
        '''Method to draw the pieces'''
        rad = SQUARE_SIZE // 2 - self.GAP
        pygame.draw.circle(win, BLACK, (self.x, self.y), rad + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), rad)
        if self.king:
            width, height = CROWN.get_size()
            win.blit(CROWN, (self.x - width // 2, self.y - height // 2))

    def move(self, row, col):
        '''Method to move a piece'''
        self.row = row
        self.col = col
        self.pos()

    def make_king(self, row):
        '''If piece can be made into king, make it into king'''
        if row == 0 and self.color == WHITE_PIECES:
            self.king = True
        elif row == 7 and self.color == BLACK_PIECES:
            self.king = True

    def valid_moves(self):
        '''Get basic moves for selected piece'''
        # Moves for all pieces
        if self.col == COLS - 1:
            self.available_moves.append(
                (self.row + self.direction, self.col - 1))
        elif self.col == 0:
            self.available_moves.append(
                (self.row + self.direction, self.col + 1))
        else:
            self.available_moves.append(
                (self.row + self.direction, self.col + 1))
            self.available_moves.append(
                (self.row + self.direction, self.col - 1))

        # Moves for kings
        temp = []
        for i in self.available_moves:
            temp.append(i)

        if self.king:
            for move in temp:
                self.available_moves.append(
                    (move[0] - 2 * self.direction, move[1]))

        # Make sure there are no out of board moves
        temp = []
        for i in self.available_moves:
            temp.append(i)

        for move in temp:
            if move[0] < 0 or move[0] > 7 or move[1] < 0 or move[1] > 7:
                self.available_moves.remove(move)

    def __repr__(self):
        if self.color == WHITE_PIECES:
            return 'White'
        else:
            return 'Black'
