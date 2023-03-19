import pygame

# BOARD DIMESIONS
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# COLORS
WHITE_PIECES = (255, 255, 255)
BLACK_PIECES = (0, 0, 0)
LIGHT_SQUARES = (240, 217, 181)
DARK_SQUARES = (139, 69, 19)
DARK_SQUARES_MOVE = (255, 215, 0)
BLACK = (0, 0, 0)
BLUE =  (0,0,255)

# DEPTH for move search
INF = float('inf')

# Crown source: http://clipart-library.com/clipart/crown-clip-art-18.htm
CROWN = pygame.transform.scale(
    pygame.image.load('files/assets/crown.jpg'), (50, 50))
