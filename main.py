import pygame
from files.constants import WIDTH, HEIGHT, BLUE, WHITE_PIECES, BLACK_PIECES, DARK_SQUARES
from files.board import Board
import time
from files.search import minimax


FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 60)
font2 = pygame.font.SysFont('Comic Sans MS', 24)


def get_click_pos(pos):
    '''Get the row and col that were clicked on'''
    col = pos[0] // 100
    row = pos[1] // 100
    return (row, col)


def end_screen(board, win):
    '''Get the end screen when game is won'''
    board.winner()
    if board.victor != None:
        textsurface = font.render(board.victor, True, BLACK_PIECES)
        size = textsurface.get_size()
        win.blit(textsurface, (400 - size[0] / 2, 400 - size[1] / 2))
        pygame.display.update()
        time.sleep(5)
        return False
    return True


def obtain_piece(board, piece):
    '''Get a piece on the board and draw the board (to see the valid moves)'''
    board.selected_piece = piece
    board.valid_moves(board.selected_piece)
    board.draw(WIN)


def get_depth():
    WIN.fill(DARK_SQUARES)
    textsurface1 = font2.render("Choose difficulty", True, WHITE_PIECES)
    size1 = textsurface1.get_size()
    WIN.blit(textsurface1, (400 - size1[0] / 2, 100))
    # pygame.draw.rect(WIN, GREY, (200, 325, 400, 150), False)
    pygame.draw.rect(WIN, WHITE_PIECES,  (190, 325, 7, 150))
    pygame.draw.rect(WIN, WHITE_PIECES,  (190, 325, 400, 7))
    pygame.draw.rect(WIN, WHITE_PIECES,  (190, 475, 407, 7))
    for i in range(1, 5):
        d = str(i)
        textsurface = font.render(d, True, WHITE_PIECES)
        size = textsurface.get_size()
        WIN.blit(textsurface, (225 + 100*(i-1), 400 - size[1] / 2))
        pygame.draw.rect(WIN, WHITE_PIECES,  (290+100*(i-1), 325, 7, 150))
    
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                x, y = pos
                if y in range(325, 325+150):
                    if x in range(200, 290):
                        return 1
                    elif x in range(300, 390):
                        return 2
                    elif x in range(400, 490):
                        return 3
                    elif x in range(500, 590):
                        return 4

def choose_players():
    WIN.fill(DARK_SQUARES)
    textsurface = font2.render("Press 1 to play against computer, 2 to play against human", True, WHITE_PIECES)
    size = textsurface.get_size()
    WIN.blit(textsurface, (400 - size[0] / 2, 100))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                elif event.key == pygame.K_2:
                    return 2 

def main():
    '''Main program for running the game'''
    run = True
    clock = pygame.time.Clock()

    # Create board
    board = Board()

    # variable to store selected piece
    piece = None
    players = choose_players()
    if players == 1:
        depth = get_depth()

    if players == 1:
        while run:
                
            clock.tick(FPS)

            end_screen(board, WIN)
            board.draw(WIN)
            # If it is black's/computer's turn
            if board.turn == BLACK_PIECES:
                evaluation, new_board = minimax(board, depth, False)
                board = new_board
                board.draw(WIN)
                run = end_screen(board, WIN)

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
                            obtain_piece(board, piece)
                        else:
                            board.change_turn()
                    else:
                        if piece == 0:
                            board.selected_piece = None
                        if piece != 0 and piece.color == board.turn:
                            obtain_piece(board, piece)

                if event.type == pygame.MOUSEBUTTONUP:
                    if board.selected_piece != None:
                        n_pos = event.pos
                        n_row, n_col = get_click_pos(n_pos)
                        board.move(n_row, n_col)
                        board.draw(WIN)

            board.draw(WIN)
            pygame.display.update()
    if players == 2:
        while run:
                
            clock.tick(FPS)

            end_screen(board, WIN)
            board.draw(WIN)
            
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
                            obtain_piece(board, piece)
                        else:
                            board.change_turn()
                    else:
                        if piece == 0:
                            board.selected_piece = None
                        if piece != 0 and piece.color == board.turn:
                            obtain_piece(board, piece)

                if event.type == pygame.MOUSEBUTTONUP:
                    if board.selected_piece != None:
                        n_pos = event.pos
                        n_row, n_col = get_click_pos(n_pos)
                        board.move(n_row, n_col)
                        board.draw(WIN)

            board.draw(WIN)
            pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
