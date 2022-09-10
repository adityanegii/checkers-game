import pygame
from files.constants import WIDTH, HEIGHT, BLUE, WHITE_PIECES, DEPTH, BLACK_PIECES, INF
from files.board import Board
import time
from files.search import minimax


FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 60)


def get_click_pos(pos):
    '''Get the row and col that were clicked on'''
    col = pos[0] // 100
    row = pos[1] // 100
    return (row, col)


def end_screen(board, win):
    '''Get the end screen when game is won'''
    board.winner()
    if board.victor != None:
        textsurface = font.render(board.victor, False, BLUE)
        size = textsurface.get_size()
        win.blit(textsurface, (400 - size[0] / 2, 400 - size[1] / 2))
        pygame.display.update()
        time.sleep(5)
        pygame.quit()


def obtain_piece(win, board, piece):
    '''Get a piece on the board and draw the board (to see the valid moves)'''
    board.selected_piece = piece
    board.valid_moves(board.selected_piece)
    board.draw(WIN)


def main():
    '''Main program for running the game'''
    run = True
    clock = pygame.time.Clock()

    # Create board
    board = Board()

    # variable to store selected piece
    piece = None
    while run:
        clock.tick(FPS)

        end_screen(board, WIN)
        board.draw(WIN)
        # If it is black's/computer's turn
        if board.turn == BLACK_PIECES:
            evaluation, new_board = minimax(board, DEPTH, False)
            board = new_board
            board.draw(WIN)
            end_screen(board, WIN)

        # To have second player as ai uncomment the next section and comment out the for loop
        # elif board.turn == WHITE_PIECES:
        #     evaluation, new_board = minimax(board, DEPTH, True)
        #     board = new_board
        #     board.draw(WIN)
        #     end_screen(board, WIN)

        # If it is white's/player's turn
        for event in pygame.event.get():

            # Quit the game
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row, col = get_click_pos(pos)
                piece = board.get_piece(row, col)

                if board.in_chain != None:
                    if row == board.in_chain.row and col == board.in_chain.col:
                        obtain_piece(WIN, board, piece)
                    else:
                        board.change_turn()
                else:
                    if piece == 0:
                        board.selected_piece = None
                    if piece != 0 and piece.color == board.turn:
                        obtain_piece(WIN, board, piece)

            if event.type == pygame.MOUSEBUTTONUP:
                if board.selected_piece != None:
                    n_pos = event.pos
                    n_row, n_col = get_click_pos(n_pos)
                    board.move(n_row, n_col)
                    board.draw(WIN)

        board.draw(WIN)
        pygame.display.update()

    pygame.quit()


main()
