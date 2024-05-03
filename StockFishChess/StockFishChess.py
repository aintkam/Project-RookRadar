import pygame
import chess
import chess.engine

# Initialize Pygame
pygame.init()

# Set up the Pygame window
WIDTH, HEIGHT = 480, 480
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess')

# Colors
WHITE = (240, 240, 240)
BLACK = (120, 120, 120)
GRAY = (169, 169, 169)
GREEN = (0, 255, 128, 0)

# Load chess piece images
piece_images = {}
for color in ['w', 'b']:
    for piece in ['p', 'r', 'n', 'b', 'q', 'k']:
        piece_images[color + piece] = pygame.image.load(f'StockFishChess/ChessPieceImages/{color}{piece}.png')

# Initialize the chess board
board = chess.Board()

# Initialize the Stockfish engine
engine = chess.engine.SimpleEngine.popen_uci("stockfish-windows-x86-64-avx2")

# Function to draw the chess board
def draw_board():
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(WINDOW, color, (col * 60, row * 60, 60, 60))

# Function to draw the chess pieces
def draw_pieces():
    for row in range(8):
        for col in range(8):
            square = chess.square(col, 7 - row)
            piece = board.piece_at(square)
            if piece is not None:
                # Construct the key with both color and piece symbol
                color = 'w' if piece.color == chess.WHITE else 'b'
                piece_key = color + piece.symbol().lower()
                piece_img = piece_images[piece_key]
                
                # Scale the image to fit within the square size
                scaled_piece_img = pygame.transform.scale(piece_img, (60, 60))
                
                # Calculate the position to center the image within the square
                x_offset = (60 - scaled_piece_img.get_width()) // 2
                y_offset = (60 - scaled_piece_img.get_height()) // 2
                
                # Blit the scaled image onto the screen
                WINDOW.blit(scaled_piece_img, pygame.Rect(col * 60 + x_offset, row * 60 + y_offset, 60, 60))

# Function to get the square from mouse coordinates
def get_square_from_mouse(pos):
    x, y = pos
    col = x // 60
    row = 7 - (y // 60)
    return chess.square(col, row)

# Function to draw a semi-transparent rectangle over a square
def draw_highlight_square_transparent(square, color=GREEN, alpha=100):
    rect = pygame.Rect(chess.square_file(square) * 60, (7 - chess.square_rank(square)) * 60, 60, 60)
    draw_transparent_rect(WINDOW, color, rect, alpha)

# Define the draw_highlight_square function
def draw_highlight_square(square, color=GREEN, alpha=100):
    rect = pygame.Rect(chess.square_file(square) * 60, (7 - chess.square_rank(square)) * 60, 60, 60)
    draw_transparent_rect(WINDOW, color, rect, alpha)

# Function to get the best move from Stockfish
def get_best_move():
    result = engine.play(board, chess.engine.Limit(time=1.0))
    return result.move

# function to draw a transparent rectangle
def draw_transparent_rect(surface, color, rect, alpha):
    temp_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    temp_surface.fill((color[0], color[1], color[2], alpha))
    surface.blit(temp_surface, rect.topleft)

selected_square = None  # Initialize selected_square variable
mouse_pos = (0,0)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if board.turn == chess.WHITE:
                # Player's turn
                pos = pygame.mouse.get_pos()
                square = get_square_from_mouse(pos)
                if selected_square is None:
                    selected_square = square
                else:
                    move = chess.Move(selected_square, square)
                    if move in board.legal_moves:
                        board.push(move)
                        selected_square = None
                    else:
                        selected_square = square
                        continue  # Skip AI move if the player's move is invalid
                # Add a small delay after the player's move
                pygame.time.wait(200)  # Adjust the delay time as needed
            else:
                # AI's turn
                best_move = get_best_move()
                if best_move is not None:  # Check if best_move is not None
                    board.push(best_move)

    # Draw the board and pieces
    draw_board()
    draw_pieces()

    # Draw the mouse position indicator
    pygame.draw.circle(WINDOW, (255, 0, 0), mouse_pos, 5)  # Draw a red circle at the mouse position

    # Player's turn: Show recommended move
    if board.turn == chess.WHITE:
        best_move = get_best_move()
        if best_move is not None:  # Check if best_move is not None
            recommended_square = best_move.from_square
            draw_highlight_square_transparent(recommended_square)

    # Check for checkmate or stalemate
    if board.is_checkmate():
        outcome_message = "Checkmate - Black Wins!" if board.turn == chess.WHITE else "Checkmate - White Wins!"
        print(outcome_message)
        running = False
    elif board.is_stalemate():
        print("Stalemate - Draw!")
        running = False

    # Update the display
    pygame.display.flip()

# Close the engine and quit Pygame
engine.quit()
pygame.quit()

