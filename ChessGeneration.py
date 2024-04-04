import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 480, 480
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
GRAY = (200, 200, 200)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

w_pawn_img = pygame.image.load("w_pawn.png")
b_pawn_img = pygame.image.load("b_pawn.png")
w_rook_img = pygame.image.load("w_rook.png")
b_rook_img = pygame.image.load("b_rook.png")
w_knight_img = pygame.image.load("w_knight.png")
b_knight_img = pygame.image.load("b_knight.png")
w_bishop_img = pygame.image.load("w_bishop.png")
b_bishop_img = pygame.image.load("b_bishop.png")
w_king_img = pygame.image.load("w_king.png")
b_king_img = pygame.image.load("b_king.png")
w_queen_img = pygame.image.load("w_queen.png")
b_queen_img = pygame.image.load("b_queen.png")

pawn_size = (SQUARE_SIZE, SQUARE_SIZE)
rook_size = (SQUARE_SIZE, SQUARE_SIZE)
knight_size = (SQUARE_SIZE, SQUARE_SIZE)
bishop_size = (SQUARE_SIZE, SQUARE_SIZE)
king_size = (SQUARE_SIZE, SQUARE_SIZE)
queen_size = (SQUARE_SIZE, SQUARE_SIZE)

w_pawn_img = pygame.transform.scale(w_pawn_img, pawn_size)
b_pawn_img = pygame.transform.scale(b_pawn_img, pawn_size)
w_rook_img = pygame.transform.scale(w_rook_img, rook_size)
b_rook_img = pygame.transform.scale(b_rook_img, rook_size)
w_knight_img = pygame.transform.scale(w_knight_img, knight_size)
b_knight_img = pygame.transform.scale(b_knight_img, knight_size)
w_bishop_img = pygame.transform.scale(w_bishop_img, bishop_size)
b_bishop_img = pygame.transform.scale(b_bishop_img, bishop_size)
w_king_img = pygame.transform.scale(w_king_img, king_size)
b_king_img = pygame.transform.scale(b_king_img, king_size)
w_queen_img = pygame.transform.scale(w_queen_img, queen_size)
b_queen_img = pygame.transform.scale(b_queen_img, queen_size)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chessboard")

def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else GRAY
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces():
    for row in range(ROWS):
        for col in range(COLS):
            if row == 1:
                screen.blit(b_pawn_img, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            elif row == 6:
                screen.blit(w_pawn_img, (col * SQUARE_SIZE, row * SQUARE_SIZE))

            elif row == 0 and col == 3:
                screen.blit(b_king_img, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            elif row == 7 and col == 3:
                screen.blit(w_king_img, (col * SQUARE_SIZE, row * SQUARE_SIZE))

            elif row == 0 and col == 4:
                screen.blit(b_queen_img, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            elif row == 7 and col == 4:
                screen.blit(w_queen_img, (col * SQUARE_SIZE, row * SQUARE_SIZE))
                 
            elif row == 0 and (col == 1 or col == 6):
                screen.blit(b_knight_img, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            elif row == 7 and (col == 1 or col == 6):
                screen.blit(w_knight_img, (col * SQUARE_SIZE, row * SQUARE_SIZE))

            elif row == 0 and (col == 2 or col == 5):
                screen.blit(b_bishop_img, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            elif row == 7 and (col == 2 or col == 5):
                screen.blit(w_bishop_img, (col * SQUARE_SIZE, row * SQUARE_SIZE))
                
            elif row == 0 and (col == 0 or col == 7):
                screen.blit(b_rook_img, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            elif row == 7 and (col == 0 or col == 7):
                screen.blit(w_rook_img, (col * SQUARE_SIZE, row * SQUARE_SIZE))

######## MAIN LOOP ########
def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        screen.fill(BLACK)
        draw_board()
        draw_pieces()
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
