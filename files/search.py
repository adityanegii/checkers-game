from .board import Board
from .evaluation import evaluate_position
from .constants import *
import pygame
from copy import deepcopy

# Variable that will let us know the board associated with the best move
reperatory = None

'''Function to find the best move for computer'''


def minimax(board, depth, maximizing):
    '''Alpha-beta pruning algorithm to find the best 'path' for computer to take without the pruning part.
    Algorithm taken from https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning#Pseudocode'''

    board.winner()
    if depth == 0 or board.victor != None:
        return evaluate_position(board), board

    # If white's turn (maximizing player)
    if maximizing:
        maxEval = -INF
        best_move = None
        for neighbour in get_neighbours(board, WHITE_PIECES):
            evaluation = minimax(neighbour, depth - 1, False)[0]
            maxEval = max(maxEval, evaluation)
            if evaluation == maxEval:
                best_move = neighbour

        return maxEval, best_move

    # If black's turn (minimizing player)
    else:
        minEval = INF
        best_move = None
        for neighbour in get_neighbours(board, BLACK_PIECES):
            evaluation = minimax(neighbour, depth - 1, True)[0]
            minEval = min(minEval, evaluation)
            if evaluation == minEval:
                best_move = neighbour

        return minEval, best_move


def get_neighbours(board, color):
    '''Get all possible boards that can be attained from a certain position by doing one move'''
    neighbours = []

    # If there is a capturing chain on, ensure that only capturing moves with selected piece can be executed
    if board.in_chain != None:

        piece = board.selected_piece
        board.valid_moves(piece)

        for move in piece.capturing_moves:
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            temp_board.selected_piece = temp_piece
            temp_board.move(move[0], move[1])
            neighbours.append(temp_board)

    else:
        for piece in board.get_all_pieces(color):

            board.valid_moves(piece)

            for move in piece.available_moves:
                temp_board = deepcopy(board)
                temp_piece = temp_board.get_piece(piece.row, piece.col)
                temp_board.selected_piece = temp_piece
                temp_board.move(move[0], move[1])
                neighbours.append(temp_board)

    return neighbours
