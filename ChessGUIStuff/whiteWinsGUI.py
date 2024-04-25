import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 300
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chess Game")

# Colors
GREEN = (12, 120, 120)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
FONT = pygame.font.Font(None, 36)

# Function to draw text on the screen
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# Function to draw the main menu screen
def draw_menu():
    screen.fill(GREEN)
    draw_text("White Wins!", FONT, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
    pygame.draw.rect(screen, BLACK, button_rect)
    draw_text("Main Menu", FONT, WHITE, button_rect.centerx, button_rect.centery)

def drawMainMenu():
    # Set up the screen dimensions
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Main Menu')

    # for fps
    clock = pygame.time.Clock()

    # defining fonts
    font = pygame.font.SysFont('arialblack', 40)

    # Create a surface for the button
    buttonSurface = pygame.Surface((150, 50))

    # Render text on the button
    text = font.render("Start!", True, (0, 0, 0))
    textRect = text.get_rect(center=(buttonSurface.get_width()/2, buttonSurface.get_height()/2))

    # Create a pygame.Rect object that represents the button's boundaries
    buttonRect = pygame.Rect(320, 420, 150, 50)  # Adjust the position as needed

    # Function to draw the other GUI screen
    def draw_other_gui():
        # Clear the screen
        screen.fill((255, 255, 255))
        
        # Draw other GUI elements
        # For example:
        # draw_text("Welcome to the other GUI!", font, (0, 0, 0), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        # Draw other elements of your GUI here
        
        # Update the display
        pygame.display.update()

    # creating the logo instance 
    img = pygame.image.load('images/Logo.png').convert()
    img = pygame.transform.scale(img, (400, 400))

    # game loop
    run = True
    while run:
        clock.tick(60)

        screen.fill((52, 78, 91))
        screen.blit(img, (200, 0))

        # event handler 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check if the mouse clicks on the button
                if buttonRect.collidepoint(event.pos):
                    print("Button clicked!")
                    # Call the function to draw the other GUI screen
                    draw_other_gui()

        # Check if the mouse is over the button. This will create the button hover effect
        if buttonRect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(buttonSurface, (127, 255, 212), (1, 1, 148, 48))
        else:
            pygame.draw.rect(buttonSurface, (0, 0, 0), (0, 0, 150, 50))
            pygame.draw.rect(buttonSurface, (255, 255, 255), (1, 1, 148, 48))
            pygame.draw.rect(buttonSurface, (0, 0, 0), (1, 1, 148, 1), 2)
            pygame.draw.rect(buttonSurface, (0, 100, 0), (1, 48, 148, 10), 2)

        # Show button text
        buttonSurface.blit(text, textRect)

        # Draw the button on the screen
        screen.blit(buttonSurface, (buttonRect.x, buttonRect.y))

        # Update the game state
        pygame.display.update()   

# Main loop
running = True
button_rect = pygame.Rect(125, 150, 150, 50)  # Button rectangle
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse_pos):
                # If the mouse clicks within the button rectangle, switch to the other GUI screen
                drawMainMenu() # Call the function to draw the other GUI

    draw_menu()

    pygame.display.flip()

pygame.quit()
sys.exit()
