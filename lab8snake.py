import pygame
import random

# Initialize Pygame library
pygame.init()

# Game configuration constants
WINDOW_SIZE = 600
CELL_DIMENSION = 30
BASE_FPS = 5

# Color palette
GRID_LIGHT = (173, 216, 230)
GRID_DARK = (25, 25, 112)
SNAKE_HEAD = (255, 0, 0)
SNAKE_BODY = (0, 128, 0)
FOOD_COLOR = (255, 215, 0)
TEXT_COLOR = (255, 200, 125)
GAME_OVER_BG = (255, 200, 200)

# Initialize game window
display_surface = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Enhanced Snake Game")
clock = pygame.time.Clock()
game_font = pygame.font.Font(None, 36)
class GridPoint:
    """Represents a position in the game grid using cell coordinates"""
    def __init__(self, x, y):
        self.x = x  # Horizontal cell position 
        self.y = y  # Vertical cell position 

class Snake:
    """Manages snake behavior including movement, growth, and collision detection"""
    def __init__(self):
        # Initial snake body configuration
        self.segments = [
            GridPoint(10, 11),
            GridPoint(10, 12),
            GridPoint(10, 13)
        ]
        self.direction = GridPoint(1, 0)  # Initial movement: right
        
    def update_position(self):
        """Updates snake position and checks for collisions"""
        # Calculate new head position based on current direction
        new_head = GridPoint(
            self.segments[0].x + self.direction.x,
            self.segments[0].y + self.direction.y
        )

        # Wall collision detection
        if not (0 <= new_head.x < WINDOW_SIZE//CELL_DIMENSION and 
                0 <= new_head.y < WINDOW_SIZE//CELL_DIMENSION):
            return True
        
        # Self-collision detection
        if any(segment.x == new_head.x and segment.y == new_head.y 
               for segment in self.segments):
            return True

        # Update snake body positions
        self.segments.insert(0, new_head)
        self.segments.pop()
        return False

    def add_segment(self):
        """Extends snake body when consuming food"""
        self.segments.append(GridPoint(
            self.segments[-1].x,
            self.segments[-1].y
        ))

    def draw(self):
        """Renders snake on the game window"""
        # Draw snake head
        pygame.draw.rect(display_surface, SNAKE_HEAD,
            (self.segments[0].x * CELL_DIMENSION,
             self.segments[0].y * CELL_DIMENSION,
             CELL_DIMENSION, CELL_DIMENSION))
        # Draw snake body segments
        for segment in self.segments[1:]:
            pygame.draw.rect(display_surface, SNAKE_BODY,
                (segment.x * CELL_DIMENSION,
                 segment.y * CELL_DIMENSION,
                 CELL_DIMENSION, CELL_DIMENSION))

class Food:
    """Manages food placement and collision detection"""
    def __init__(self, snake):
        self.position = self.generate_position(snake)
        
    def generate_position(self, snake):
        """Creates new food position ensuring it doesn't overlap with snake"""
        while True:
            new_pos = GridPoint(
                random.randint(0, (WINDOW_SIZE//CELL_DIMENSION)-1),
                random.randint(0, (WINDOW_SIZE//CELL_DIMENSION)-1)
            )
            # Ensure food doesn't spawn on snake
            if not any(segment.x == new_pos.x and segment.y == new_pos.y 
                      for segment in snake.segments):
                return new_pos

    def draw(self):
        """Renders food on the game window"""
        pygame.draw.rect(display_surface, FOOD_COLOR,
            (self.position.x * CELL_DIMENSION,
             self.position.y * CELL_DIMENSION,
             CELL_DIMENSION, CELL_DIMENSION))

def create_game_grid():
    """Draws the checkerboard pattern game background"""
    for row in range(WINDOW_SIZE//CELL_DIMENSION):
        for col in range(WINDOW_SIZE//CELL_DIMENSION):
            # Alternate colors for checkerboard pattern
            cell_color = GRID_LIGHT if (row + col) % 2 == 0 else GRID_DARK
            pygame.draw.rect(display_surface, cell_color,
                (col*CELL_DIMENSION, row*CELL_DIMENSION,
                 CELL_DIMENSION, CELL_DIMENSION))

def run_game():
    """Main game loop controlling game flow and state"""
    current_speed = BASE_FPS
    snake = Snake()
    food = Food(snake)
    player_score = 0
    current_level = 1
    is_game_over = False

    while not is_game_over:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
                
            if event.type == pygame.KEYDOWN:
                # Direction controls with prevention of 180-degree turns
                if event.key == pygame.K_RIGHT and snake.direction.x != -1:
                    snake.direction = GridPoint(1, 0)
                elif event.key == pygame.K_LEFT and snake.direction.x != 1:
                    snake.direction = GridPoint(-1, 0)
                elif event.key == pygame.K_DOWN and snake.direction.y != -1:
                    snake.direction = GridPoint(0, 1)
                elif event.key == pygame.K_UP and snake.direction.y != 1:
                    snake.direction = GridPoint(0, -1)

        # Game state updates
        is_game_over = snake.update_position()
        
        # Food consumption check
        if (snake.segments[0].x == food.position.x and 
            snake.segments[0].y == food.position.y):
            player_score += 1
            snake.add_segment()
            food = Food(snake)
            
            # Level progression system
            if player_score % 4 == 0:
                current_level += 1
                current_speed += 2  # Increase difficulty

        # Rendering
        create_game_grid()
        snake.draw()
        food.draw()
        
        score_label = game_font.render(
            f"Score: {player_score}  Level: {current_level}", 
            True, TEXT_COLOR)
        display_surface.blit(score_label, (10, 10))
        
        pygame.display.update()
        clock.tick(current_speed)

    # Game over sequence
    display_surface.fill(GAME_OVER_BG)
    final_score_text = game_font.render(
        f"Final Score: {player_score}", True, TEXT_COLOR)
    display_surface.blit(final_score_text, 
        (WINDOW_SIZE//2 - 100, WINDOW_SIZE//2))
    pygame.display.update()
    pygame.time.wait(3000)

if __name__ == "__main__":
    run_game()
    pygame.quit()