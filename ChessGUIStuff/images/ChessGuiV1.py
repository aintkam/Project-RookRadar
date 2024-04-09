import pygame

pygame.init()

# for fps
clock = pygame.time.Clock()

# creating the game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Main Menu')

# variables
menu = False

# defining fonts
font = pygame.font.SysFont('arialblack', 40)

# Create a surface for the button
buttonSurface = pygame.Surface((150, 50))

# Render text on the button
text = font.render("Start!", True, (0, 0, 0))
textRect = text.get_rect(center=(buttonSurface.get_width()/2, buttonSurface.get_height()/2))

# Create a pygame.Rect object that represents the button's boundaries
buttonRect = pygame.Rect(320, 420, 150, 50)  # Adjust the position as needed

# creating the logo instance 
img = pygame.image.load('ChessGUIStuff/images/Logo.png').convert()
img = pygame.transform.scale(img, (400, 400))

# define colors
TEXT_COLOR = (255, 255, 255)

# game loop
run = True
while (run):

    clock.tick(60)

    screen.fill((52, 78, 91))
    screen.blit(img,(200,0))

    # event handler 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
   # Quit the game
            pygame.quit()

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
   # Call the on_mouse_button_down() function
        if buttonRect.collidepoint(event.pos):
            print("Button clicked!")

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

pygame.quit()






