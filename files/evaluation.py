import pygame
from .constants import *
#from .board import board

KING_POINTS = 4
PIECE_POINTS = 2
CAPTURE_POINTS = -1
ROW_POINTS = 0.1


def adj_squares(piece):
    '''Get the adjacent squares of a piece'''
    return [(piece.row + 1, piece.col + 1), (piece.row + 1, piece.col - 1), (piece.row - 1, piece.col - 1), (piece.row - 1, piece.col + 1)]


def possible_capture(piece, board):
    '''Determine whether a piece can be captured currently'''
    adj_square = adj_squares(piece)
    for a_square in adj_square:
        row = a_square[0]                   # Row of adjacent square
        col = a_square[1]                   # Col of adjacent square

        if 0 < row < ROWS and 0 < col < COLS:
            adj_piece = board.board[row][col]

            if adj_piece != 0:
                # If adjacent piece is of different color (so it can capture)
                if adj_piece.color != board.turn:

                    # Square that adj_piece would jump to capture
                    #a_row = 2*piece.row - adj_piece.row
                    #a_col = 2*piece.col - adj_piece.col

                    board.valid_moves(adj_piece)
                    for move in adj_piece.capturing_moves:
                        if move in adj_square:
                            return True
                    return False
                    '''
                    if 0 < a_row < ROWS and 0 < a_col < COLS:
                        if adj_piece.king == True:
                            if board.board[a_row][a_col] == 0:
                                return True
                        else:
                            if adj_piece.color == BLACK_PIECES:
                                if adj_piece.row > piece.row and board.board[a_row][a_col] == 0:
                                    return True
                            else:
                                if adj_piece.row < piece.row and board.board[a_row][a_col] == 0:
                                    return True'''

    return False


def point_accumulation(piece):
    '''Count accumulated points for pieces only'''
    if piece.king == True:
        return KING_POINTS
    else:
        return PIECE_POINTS + piece.row * ROW_POINTS


def evaluate_position(board):
    '''Evaluate the current position of a board with the following conditions:
    1. Each piece is 2 point + 0.1 * the row they are on compared to their back row (pieces closer to becoming king are worth more)
    2. Each king is worth 4 points
    3. Exposed pieces (pieces that can be taken) are worth - 0.5
    Black's points are then subtracted from White's points. If the result is positive, 
    White has the advantage, and if the result is negative, Black has the advantage'''

    board.winner()
    if board.victor == 'Black wins':
        return -INF
    elif board.victor == 'White wins':
        return INF
    elif board.victor == "It's a tie":
        return 0

    white_points = 0
    black_points = 0

    # VARIABLES USED FOR DEBUGGING
    #b_king_points = 0
    #b_piece_points = 0
    #b_capture_points = 0

    #w_king_points = 0
    #w_piece_points = 0
    #w_capture_points = 0

    for b_row in board.board:
        for piece in b_row:
            if piece != 0:

                capture_possible = possible_capture(piece, board)

                if piece.color == BLACK_PIECES:
                    black_points -= point_accumulation(piece)

                    if capture_possible:
                        black_points -= CAPTURE_POINTS
                        # b_capture_points -= CAPTURE_POINTS

                elif piece.color == WHITE_PIECES:

                    # To ensure the count is good since white pieces go from row 7 to 0
                    if capture_possible:
                        white_points += CAPTURE_POINTS
                        # w_capture_points += CAPTURE_POINTS

                    if piece.king == True:
                        white_points += point_accumulation(piece)

                    else:
                        # Equation made from exel
                        white_points += 4.7 - point_accumulation(piece)

    #print(round(white_points + black_points, 2))
    return round(white_points + black_points, 2)
