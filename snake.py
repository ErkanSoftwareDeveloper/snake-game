# ---------------------
# --- LIBRARIES ---
# ---------------------
import pygame  # Library for creating games and multimedia applications
import sys     # Provides access to system-specific functions (like exiting)
import random  # For generating random numbers (used for food positions)

# ---------------------
# --- INITIALIZATION ---
# ---------------------
pygame.init()  # Initialize all imported Pygame modules

# ---------------------
# --- MUSIC SETUP ---
# ---------------------
pygame.mixer.init()  # Initialize the mixer module for sound
pygame.mixer.music.load('snake.mp3')  # Load background music file
pygame.mixer.music.play(-1)  # Play music indefinitely (-1 loop)
pygame.mixer.music.set_volume(0.5)  # Set music volume to 50%

# ---------------------
# --- SCREEN SETUP ---
# ---------------------
width, height = 600, 400  # Set screen width and height
screen = pygame.display.set_mode((width, height))  # Create game window
pygame.display.set_caption("🐍 Snake Game")  # Set window title

# ---------------------
# --- COLORS ---
# ---------------------
GREEN = (170, 215, 81)  # Light green (background)
DARK_GREEN = (0, 100, 0)  # Dark green (snake)
RED = (255, 0, 0)  # Red (food)
WHITE = (255, 255, 255)  # White (text)
BLACK = (0, 0, 0)  # Black (not used currently)
GRAY = (60, 60, 60)  # Gray (game over screen)

# ---------------------
# --- FPS CONTROL ---
# ---------------------
clock = pygame.time.Clock()  # Create clock object to control frame rate
snake_speed = 10  # Set initial snake speed (frames per second)

# ---------------------
# --- SNAKE INITIAL STATE ---
# ---------------------
snake_pos = [100, 50]  # Snake head initial position (x, y)
snake_body = [[100, 50], [90, 50], [80, 50]]  # Initial snake body segments
snake_direction = 'RIGHT'  # Initial movement direction

# ---------------------
# --- FOOD INITIAL STATE ---
# ---------------------
food_pos = [random.randrange(1, (width // 10)) * 10,
            random.randrange(1, (height // 10)) * 10]  # Random food position
food_spawn = True  # Boolean flag to track if food is present

# ---------------------
# --- SCORE ---
# ---------------------
score = 0  # Initial score

# ---------------------
# --- FONTS ---
# ---------------------
font = pygame.font.SysFont('arial', 25)  # Font for score display
game_over_font = pygame.font.SysFont(
    'arial', 40, True)  # Bold font for game over

# ---------------------
# --- FUNCTIONS ---
# ---------------------


def show_score():
    """Display the current score on the screen"""
    score_text = font.render(f"Score: {score}", True, WHITE)  # Render text
    screen.blit(score_text, [10, 10])  # Draw text at top-left corner


def draw_button(text, x, y, w, h, color, hover_color):
    """Draw a clickable button and detect clicks"""
    mouse = pygame.mouse.get_pos()  # Get mouse position
    click = pygame.mouse.get_pressed()  # Get mouse button states
    if x + w > mouse[0] > x and y + h > mouse[1] > y:  # Check if mouse is over button
        pygame.draw.rect(screen, hover_color, (x, y, w, h))  # Draw hover color
        if click[0] == 1:  # Left mouse button clicked
            return True
    else:
        pygame.draw.rect(screen, color, (x, y, w, h))  # Draw normal color
    text_surface = font.render(text, True, WHITE)  # Render button text
    text_rect = text_surface.get_rect(
        center=(x + w / 2, y + h / 2))  # Center text
    screen.blit(text_surface, text_rect)  # Draw text
    return False  # Return False if button not clicked


def game_over():
    """Game over screen with score and options to play again or exit"""
    pygame.mixer.music.stop()  # Stop background music
    while True:  # Loop until player exits or restarts
        screen.fill(GRAY)  # Fill background with gray
        text = game_over_font.render(f"Game Over! Score: {score}", True, WHITE)
        text_rect = text.get_rect(center=(width / 2, height / 3))
        screen.blit(text, text_rect)  # Draw game over text

        # Draw buttons
        again = draw_button("PLAY AGAIN", width / 2 - 100,
                            height / 2, 200, 50, DARK_GREEN, GREEN)
        exit_game = draw_button("EXIT", width / 2 - 100,
                                height / 2 + 70, 200, 50, RED, (255, 100, 100))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Window close button clicked
                pygame.quit()
                sys.exit()

        if again:  # Restart game selected
            main_game()  # Call main game function
        if exit_game:  # Exit game selected
            pygame.quit()
            sys.exit()

        pygame.display.update()  # Update screen
        clock.tick(15)  # Limit frame rate for menu


def main_game():
    """Main game loop"""
    global snake_pos, snake_body, snake_direction, food_pos, food_spawn, score

    # Reset game state
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    snake_direction = 'RIGHT'
    food_pos = [random.randrange(1, (width // 10)) * 10,
                random.randrange(1, (height // 10)) * 10]
    food_spawn = True
    score = 0

    pygame.mixer.music.play(-1)  # Restart background music

    while True:  # Main game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Window close
                pygame.quit()
                sys.exit()

            # Direction control
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_direction != "DOWN":
                    snake_direction = 'UP'
                elif event.key == pygame.K_DOWN and snake_direction != "UP":
                    snake_direction = 'DOWN'
                elif event.key == pygame.K_LEFT and snake_direction != "RIGHT":
                    snake_direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and snake_direction != "LEFT":
                    snake_direction = 'RIGHT'

        # Move snake head
        if snake_direction == 'UP':
            snake_pos[1] -= 10
        if snake_direction == 'DOWN':
            snake_pos[1] += 10
        if snake_direction == 'LEFT':
            snake_pos[0] -= 10
        if snake_direction == 'RIGHT':
            snake_pos[0] += 10

        # Add new head to snake body
        snake_body.insert(0, list(snake_pos))

        # Food collision
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            score += 10  # Increase score
            food_spawn = False  # Spawn new food
        else:
            snake_body.pop()  # Remove last segment to move snake

        # Spawn new food if eaten
        if not food_spawn:
            food_pos = [random.randrange(1, (width // 10)) * 10,
                        random.randrange(1, (height // 10)) * 10]
        food_spawn = True

        # Check collision with walls
        if snake_pos[0] < 0 or snake_pos[0] >= width or snake_pos[1] < 0 or snake_pos[1] >= height:
            game_over()

        # Check collision with self
        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_over()

        # Draw background
        screen.fill(GREEN)

        # Draw snake
        for block in snake_body:
            pygame.draw.rect(screen, DARK_GREEN, pygame.Rect(
                block[0], block[1], 10, 10))

        # Draw food
        pygame.draw.rect(screen, RED, pygame.Rect(
            food_pos[0], food_pos[1], 10, 10))

        # Show score
        show_score()

        pygame.display.update()  # Update the screen
        clock.tick(snake_speed)  # Control game speed


# ---------------------
# --- START GAME ---
# ---------------------
main_game()  # Start the main game loop
