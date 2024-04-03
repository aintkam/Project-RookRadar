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
pawn_size = (SQUARE_SIZE, SQUARE_SIZE)
w_pawn_img = pygame.transform.scale(w_pawn_img, pawn_size)
b_pawn_img = pygame.transform.scale(b_pawn_img, pawn_size)

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
