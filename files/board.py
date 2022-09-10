import pygame
from .constants import *
from .piece import Piece


class Board:
    '''Class representing a checkers board'''

    def __init__(self):
        '''Initialising the board'''
        self.turn = WHITE_PIECES
        self.board = []
        self.selected_piece = None

        # If in_chain is not None, that means that it is a piece which is currently in a capture chain
        self.in_chain = None

        # Keep track of the number of pieces
        self.white_pieces = 12
        self.black_pieces = 12
        self.white_kings = 0
        self.black_kings = 0

        # To count number of moves done from a certain point to determine tie
        self.tie_counter = 0
        self.move_counter = 0

        self.victor = None

        self.prev_move = None

        for row in range(ROWS):
            tmp = []
            for col in range(COLS):
                if col % 2 != row % 2:
                    if row < 3:
                        tmp.append(Piece(row, col, BLACK_PIECES))
                    elif row > 4:
                        tmp.append(Piece(row, col, WHITE_PIECES))
                    else:
                        tmp.append(0)

                else:
                    tmp.append(0)

            self.board.append(tmp)

    def update(self, board):
        '''Method to update board with another board'''
        self.board = board.board
        self.count_pieces()
        board.change_turn()

    def draw_squares(self, win):
        '''Draw the squares of the board'''
        win.fill(LIGHT_SQUARES)
        for row in range(ROWS):
            for col in range(COLS):
                if row % 2 != col % 2:
                    pygame.draw.rect(
                        win, DARK_SQUARES, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        
        if self.prev_move != None:
            o, d = self.prev_move
            oR, oC = o
            dR, dC = d
            if (oR + oC) % 2 == 0:
                pygame.draw.rect(
                    win, LIGHT_SQUARES_MOVE, (oC*SQUARE_SIZE, oR*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            else:
                pygame.draw.rect(
                    win, DARK_SQUARES_MOVE, (oC*SQUARE_SIZE, oR*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            if (dR + dC) % 2 == 0:
                pygame.draw.rect(
                    win, LIGHT_SQUARES_MOVE, (dC*SQUARE_SIZE, dR*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            else:
                pygame.draw.rect(
                    win, DARK_SQUARES_MOVE, (dC*SQUARE_SIZE, dR*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


    def draw(self, win):
        '''Draw the board'''
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)
        if self.selected_piece != None:
            self.draw_valid_moves(win)

    def change_turn(self):
        '''Change turn'''
        self.count_pieces()
        self.in_chain = None
        self.selected_piece = None
        self.move_counter += 0.5
        if self.turn == BLACK_PIECES:
            self.turn = WHITE_PIECES
        else:
            self.turn = BLACK_PIECES

    def move(self, row, col):
        '''Move a piece to row, col'''
        pos = (row, col)
        if pos in self.selected_piece.available_moves:
            origin = self.selected_piece.row, self.selected_piece.col
            self.board[self.selected_piece.row][self.selected_piece.col], self.board[row][
                col] = self.board[row][col], self.board[self.selected_piece.row][self.selected_piece.col]

            # If capturing a piece
            if pos in self.selected_piece.capturing_moves:
                self.in_chain = self.selected_piece
                self.capture(row, col)

            # If not capturing a piece
            else:
                self.selected_piece.move(row, col)

            # Check if king can be made
            self.selected_piece.make_king(row)

            if self.in_chain == None:
                self.change_turn()
            
            self.prev_move = origin, pos
        else:
            self.selected_piece = None
        

    def capture(self, row, col):
        '''Capture a piece'''
        difference = ((row - self.selected_piece.row) // 2,
                      (col - self.selected_piece.col) // 2)
        self.board[row - difference[0]][col - difference[1]] = 0
        self.selected_piece.move(row, col)

        # Continue if capture chain is possible
        if self.in_chain.row != (0 or 7):
            self.in_chain.valid_moves()
            self.valid_moves(self.in_chain)
            if len(self.in_chain.capturing_moves) > 0:
                self.selected_piece.available_moves = self.in_chain.capturing_moves
            else:
                self.in_chain = None
        else:
            self.in_chain = None

    def get_piece(self, row, col):
        '''Method to get the piece at a certain row, col'''
        # Reset available/capturing moves since new piece has been selected
        return self.board[row][col]

    def valid_moves(self, piece):
        '''Get all valid moves for selected piece'''
        piece.available_moves = []
        piece.capturing_moves = []
        # Moves for all pieces
        piece.valid_moves()

        # Find adjacent pieces to avoid collision
        adj_pieces = self.adj_pieces(piece)
        for adj in adj_pieces:
            if adj in piece.available_moves:
                piece.available_moves.remove(adj)

        # Find capturing moves and remove colliding moves
        self.capture_moves(piece, adj_pieces)

    def capture_moves(self, piece, adj_pieces):
        '''Find possible captures'''
        # Check for captures
        if adj_pieces != None:
            for adj in adj_pieces:

                # Check if adj piece is opposition color
                if self.board[adj[0]][adj[1]].color != piece.color:
                    difference = (adj[0] - piece.row, adj[1] - piece.col)

                    # Check to see if capture is possible
                    if -1 < (adj[0] + difference[0]) < ROWS and -1 < (adj[1] + difference[1]) < COLS:
                        if self.board[adj[0] + difference[0]][adj[1] + difference[1]] == 0:
                            piece.available_moves.append(
                                (adj[0] + difference[0], adj[1] + difference[1]))
                            piece.capturing_moves.append(
                                (adj[0] + difference[0], adj[1] + difference[1]))

    def adj_pieces(self, piece):
        '''Find all adjacent pieces'''
        adj_piece = []
        for move in piece.available_moves:
            if self.board[move[0]][move[1]] != 0:
                adj_piece.append(move)
        return adj_piece

    def draw_valid_moves(self, win):
        '''Draw all valid moves for all moves'''
        self.valid_moves(self.selected_piece)
        if self.in_chain != None:
            self.selected_piece.available_moves = self.selected_piece.capturing_moves

        for move in self.selected_piece.available_moves:
            pygame.draw.circle(
                win, BLUE, (move[1] * SQUARE_SIZE + 50, move[0] * SQUARE_SIZE + 50), 20)

    def count_pieces(self):
        '''Keep track of the number of pieces/kings of each color after every move'''
        self.white_kings = 0
        self.black_kings = 0
        self.white_pieces = 0
        self.black_pieces = 0
        for square in self.board:
            for piece in square:
                if piece != 0:
                    if piece.color == BLACK_PIECES:
                        if piece.king:
                            self.black_kings += 1
                        else:
                            self.black_pieces += 1

                    elif piece.color == WHITE_PIECES:
                        if piece.king:
                            self.white_kings += 1
                        else:
                            self.white_pieces += 1

        # If both white and black have less than 4 pieces, trigger the count
        if self.white_pieces + self.white_kings and self.black_kings + self.black_pieces < 4:
            self.tie_counter += 0.5

    def get_all_pieces(self, color):
        '''Get all pieces on board of a certain color'''

        pieces = []

        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] != 0:
                    if self.board[row][col].color == color:
                        pieces.append(self.board[row][col])

        return pieces

    def winner(self):
        '''Find if someone has won'''
        if self.white_pieces == self.white_kings == 0:
            self.victor = 'Black wins'
        elif self.black_pieces == self.black_kings == 0:
            self.victor = 'White wins'
        # If 30 moves have gone while both sides have less than 4 pieces or 70 moves have gone by
        elif self.tie_counter > 30 or self.move_counter > 70:
            self.victor = "It's a tie"
        self.tie_winner()

    def tie_winner(self):
        '''If a player has been forced into a position where they cannot move, they lose'''
        moves = []

        for piece in self.get_all_pieces(self.turn):
            self.valid_moves(piece)
            for move in piece.available_moves:
                moves.append(move)

        if len(moves) == 0:
            if self.turn == WHITE_PIECES:
                self.victor = 'Black wins'
            else:
                self.victor = 'White wins'
