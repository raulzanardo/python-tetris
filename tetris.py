import sys
import pygame
import random
import argparse

pygame.init()
pygame.joystick.init()

# Check for joysticks
joystick_count = pygame.joystick.get_count()
if joystick_count > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Joystick {joystick.get_name()} initialized")
else:
    print("No joysticks found")


# Screen dimensions
WIDTH, HEIGHT = 192, 128
GRID_SIZE = 2

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
SHADOW_COLOR = (100, 100, 100)
COLORS = [RED, BLUE, GREEN]

# Tetromino shapes
SHAPES = [
    [
        ['.....',
         '.....',
         '.....',
         'OOOO.',
         '.....'],
        ['.....',
         '..O..',
         '..O..',
         '..O..',
         '..O..']
    ],
    [
        ['.....',
         '.....',
         '..O..',
         '.OOO.',
         '.....'],
        ['.....',
         '..O..',
         '.OO..',
         '..O..',
         '.....'],
        ['.....',
         '.....',
         '.OOO.',
         '..O..',
         '.....'],
        ['.....',
         '..O..',
         '..OO.',
         '..O..',
         '.....']
    ],
    [
        [
            '.....',
            '.....',
            '..OO.',
            '.OO..',
            '.....'],
        ['.....',
         '.....',
         '.OO..',
         '..OO.',
         '.....'],
        ['.....',
         '.O...',
         '.OO..',
         '..O..',
         '.....'],
        ['.....',
         '..O..',
         '.OO..',
         '.O...',
         '.....']
    ],
    [
        ['.....',
         '..O..',
         '..O.',
         '..OO.',
         '.....'],
        ['.....',
         '...O.',
         '.OOO.',
         '.....',
         '.....'],
        ['.....',
         '.OO..',
         '..O..',
         '..O..',
         '.....'],
        ['.....',
         '.....',
         '.OOO.',
         '.O...',
         '.....']
    ],
]


class Tetromino:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        # You can choose different colors for each shape
        self.color = random.choice(COLORS)
        self.rotation = 0


class Tetris:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.current_piece = self.new_piece()
        self.game_over = False
        self.game_over_time = None
        self.score = 0  # Add score attribute

    def new_piece(self):
        # Choose a random shape
        shape = random.choice(SHAPES)
        # Center spawn considering 5x5 shape templates
        spawn_x = max(0, (self.width - 5) // 2)
        return Tetromino(spawn_x, 0, shape)

    def valid_move(self, piece, x, y, rotation):
        """Check if the piece can move to the given position"""
        grid_h = self.height
        grid_w = self.width
        shape = piece.shape[(piece.rotation + rotation) % len(piece.shape)]
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell == 'O':
                    new_x = piece.x + j + x
                    new_y = piece.y + i + y
                    # Check horizontal and vertical bounds
                    if new_x < 0 or new_x >= grid_w or new_y < 0 or new_y >= grid_h:
                        return False
                    # Check collision with existing blocks
                    if self.grid[new_y][new_x] != 0:
                        return False
        return True

    def clear_lines(self):
        """Clear the lines that are full and return the number of cleared lines"""
        lines_cleared = 0
        for i, row in enumerate(self.grid[:-1]):
            if all(cell != 0 for cell in row):
                lines_cleared += 1
                del self.grid[i]
                self.grid.insert(0, [0 for _ in range(self.width)])
        return lines_cleared

    def lock_piece(self, piece):
        """Lock the piece in place and create a new piece"""
        for i, row in enumerate(piece.shape[piece.rotation % len(piece.shape)]):
            for j, cell in enumerate(row):
                if cell == 'O':
                    self.grid[piece.y + i][piece.x + j] = piece.color
        # Clear the lines and update the score
        lines_cleared = self.clear_lines()
        # Update the score based on the number of cleared lines
        self.score += lines_cleared * 100
        # Create a new piece
        self.current_piece = self.new_piece()
        # Check if the game is over
        if not self.valid_move(self.current_piece, 0, 0, 0):
            self.game_over = True
            # Record the time the game ended (milliseconds)
            try:
                self.game_over_time = pygame.time.get_ticks()
            except Exception:
                self.game_over_time = None
        return lines_cleared

    def update(self):
        """Move the tetromino down one cell"""
        if not self.game_over:
            if self.valid_move(self.current_piece, 0, 1, 0):
                self.current_piece.y += 1
            else:
                self.lock_piece(self.current_piece)

    def draw(self, screen):
        """Draw the grid and the current piece"""
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        screen, cell, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))

        if self.current_piece:
            # Draw ghost/shadow at landing position (considers locked pieces)
            ghost_dy = 0
            # find how far down the piece can go
            while self.valid_move(self.current_piece, 0, ghost_dy + 1, 0):
                ghost_dy += 1
            for i, row in enumerate(self.current_piece.shape[self.current_piece.rotation % len(self.current_piece.shape)]):
                for j, cell in enumerate(row):
                    if cell == 'O':
                        gx = (self.current_piece.x + j) * GRID_SIZE
                        gy = (self.current_piece.y + i + ghost_dy) * GRID_SIZE
                        pygame.draw.rect(screen, SHADOW_COLOR,
                                         (gx, gy, GRID_SIZE - 1, GRID_SIZE - 1))

            for i, row in enumerate(self.current_piece.shape[self.current_piece.rotation % len(self.current_piece.shape)]):
                for j, cell in enumerate(row):
                    if cell == 'O':
                        pygame.draw.rect(screen, self.current_piece.color, ((
                            self.current_piece.x + j) * GRID_SIZE, (self.current_piece.y + i) * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))


def draw_score(screen, score, x, y):
    """Draw the score on the screen"""
    # Make font size 10% of the screen height for a smaller score display
    font_size = max(1, int(HEIGHT * 0.10))
    font = pygame.font.Font(None, font_size)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (x, y))


def draw_game_over(screen):
    """Draw the game over text centered on the screen"""
    # Use a font size proportional to screen height
    font_size = max(12, int(HEIGHT * 0.15))
    font = pygame.font.Font(None, font_size)
    text = font.render("Game Over", True, RED)
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, rect)


def main():
    # Parse command-line args for pixel size
    parser = argparse.ArgumentParser(
        description="Play tiny Tetris; set pixel size with -p/--pixel-size")
    # Ensure we reference the module-level GRID_SIZE (avoid local shadowing)
    global GRID_SIZE
    parser.add_argument('-p', '--pixel-size', type=int, default=GRID_SIZE,
                        help='Size in pixels for each grid cell (integer >= 1)')
    args = parser.parse_args()
    GRID_SIZE = max(1, int(args.pixel_size))
    # Initialize pygame
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Tetris')
    # Create a clock object
    clock = pygame.time.Clock()
    # Create a Tetris object
    game = Tetris(WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE)
    fall_time = 0
    fall_speed = 50  # You can adjust this value to change the falling speed, it's in milliseconds
    while True:
        # Fill the screen with black
        screen.fill(BLACK)
        # Track whether a key was pressed this frame
        keydown_event = False
        for event in pygame.event.get():
            # Check for the QUIT event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                keydown_event = True

            # Add joystick button and axis events
            if event.type == pygame.JOYAXISMOTION:
                # Axis 0: Left/Right
                if event.axis == 0:
                    if event.value < -0.5:  # Left
                        if game.valid_move(game.current_piece, -1, 0, 0):
                            game.current_piece.x -= 1
                    elif event.value > 0.5:  # Right
                        if game.valid_move(game.current_piece, 1, 0, 0):
                            game.current_piece.x += 1
                # Axis 1: Up/Down
                elif event.axis == 1:
                    if event.value > 0.5:  # Down
                        if game.valid_move(game.current_piece, 0, 1, 0):
                            game.current_piece.y += 1

            # Handle D-pad / hat (digital directionals)
            if event.type == pygame.JOYHATMOTION:
                try:
                    hat_x, hat_y = event.value
                except Exception:
                    # Older pygame variants may pack hat differently
                    hat_x, hat_y = event.value[0], event.value[1]
                # Horizontal movement
                if hat_x < 0:
                    if game.valid_move(game.current_piece, -1, 0, 0):
                        game.current_piece.x -= 1
                elif hat_x > 0:
                    if game.valid_move(game.current_piece, 1, 0, 0):
                        game.current_piece.x += 1
                # Vertical: down for soft drop, up for rotate
                if hat_y < 0:  # down
                    if game.valid_move(game.current_piece, 0, 1, 0):
                        game.current_piece.y += 1
                elif hat_y > 0:  # up -> rotate
                    if game.valid_move(game.current_piece, 0, 0, 1):
                        game.current_piece.rotation += 1

            if event.type == pygame.JOYBUTTONDOWN:
                # Button 0 (A) or Button 1 (B) for rotation
                if event.button == 0 or event.button == 1:
                    if game.valid_move(game.current_piece, 0, 0, 1):
                        game.current_piece.rotation += 1
                # Button 2 (X) for hard drop
                elif event.button == 2:
                    while game.valid_move(game.current_piece, 0, 1, 0):
                        game.current_piece.y += 1
                    game.lock_piece(game.current_piece)

            # If any keydown while game over, restart immediately
            if event.type == pygame.KEYDOWN and game.game_over:
                game = Tetris(WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE)
                fall_time = 0

        # Get the number of milliseconds since the last frame
        delta_time = clock.get_rawtime()
        # Add the delta time to the fall time
        fall_time += delta_time
        if fall_time >= fall_speed:
            # Move the piece down
            game.update()
            # Reset the fall time
            fall_time = 0
        # Draw the score on the screen
        draw_score(screen, game.score, 10, 10)
        # Draw the grid and the current piece
        game.draw(screen)
        if game.game_over:
            # Draw the centered "Game Over" message
            draw_game_over(screen)
            # Ensure we have a recorded end time
            if game.game_over_time is None:
                try:
                    game.game_over_time = pygame.time.get_ticks()
                except Exception:
                    game.game_over_time = None
            # Auto-restart after 5 seconds
            if game.game_over_time is not None and pygame.time.get_ticks() - game.game_over_time >= 5000:
                game = Tetris(WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE)
                fall_time = 0
        # Update the display
        pygame.display.flip()
        # Set the framerate
        clock.tick(60)


if __name__ == "__main__":
    main()
