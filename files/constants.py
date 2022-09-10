import pygame

# BOARD DIMESIONS
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# COLORS
WHITE_PIECES = (252, 242, 239)
BLACK_PIECES = (49, 17, 8)
LIGHT_SQUARES = (230, 195, 165)
DARK_SQUARES = (181, 101, 29)
DARK_SQUARES_MOVE = (200, 200, 36)
LIGHT_SQUARES_MOVE = (255, 225, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)

# DEPTH for move search
DEPTH = 2
INF = float('inf')

# Crown source: http://clipart-library.com/clipart/crown-clip-art-18.htm
CROWN = pygame.transform.scale(
    pygame.image.load('C:/Users/negia/Desktop/python projects/CHECKERS/files/assets/crown.jpg'), (50, 50))
