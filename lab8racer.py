# Import necessary modules
import pygame, sys
from pygame.locals import *
import random, time

# Initialize Pygame and its mixer module
pygame.init()
pygame.mixer.init()

# Load and play background music
pygame.mixer.music.load("images for racer/background.wav")
pygame.mixer.music.set_volume(0.3)  # volume of the music
pygame.mixer.music.play(-1)  # -1 makes the music loop indefinitely

# Set up FPS (Frames Per Second) controller
FPS = 60
FramePerSec = pygame.time.Clock()

# Define color constants
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game configuration variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5      # Initial game speed
SCORE = 0      # Player score
COIN_COUNT = 0 # Collected coins counter

# Set up fonts for UI elements
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over_text = font.render("Game Over", True, BLACK)

# Load background image
background = pygame.image.load("images for racer/AnimatedStreet.png")

# Create the game window
DISPLAYSURF = pygame.display.set_mode((400, 600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Street Racer")

class Enemy(pygame.sprite.Sprite):
    """Enemy vehicle that moves down the screen and respawns at top"""
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("images for racer/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        """Handles enemy movement and respawning"""
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.bottom > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Coin(pygame.sprite.Sprite):
    """Collectible coin that can be picked up by player"""
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images for racer/coin.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.respawn()

    def respawn(self):
        """Places coin at random position on screen"""
        self.rect.topleft = (random.randint(0, SCREEN_WIDTH - self.rect.width), 
                             random.randint(0, SCREEN_HEIGHT - self.rect.height))

class Player(pygame.sprite.Sprite):
    """Player-controlled vehicle with arrow key movement"""
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("images for racer/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        self.speed = 5

    def move(self):
        """Processes keyboard input for player movement"""
        pressed_keys = pygame.key.get_pressed()
        
        # Handle horizontal movement with boundary checks
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-self.speed, 0)
        if self.rect.right < SCREEN_WIDTH:        
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(self.speed, 0)
        # Handle vertical movement with boundary checks
        if self.rect.top > 0:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -self.speed + 2)
        if self.rect.bottom < SCREEN_HEIGHT:
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, self.speed - 2)

# Initialize game objects
P1 = Player()
E1 = Enemy()
coins = pygame.sprite.Group()

# Create initial coins
for _ in range(3):
     coins.add(Coin())

# Create sprite groups
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1)
all_sprites.add(*coins)

# Create speed increase event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)  # Trigger every second

# Main game loop
while True:
    # Event processing
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5  # Gradually increase difficulty
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Draw background
    DISPLAYSURF.blit(background, (0, 0))

    # Display UI information
    score_surface = font_small.render(f"Score: {SCORE}", True, BLACK)
    coin_surface = font_small.render(f"Coins: {COIN_COUNT}", True, BLACK)
    DISPLAYSURF.blit(score_surface, (10, 10))
    DISPLAYSURF.blit(coin_surface, (SCREEN_WIDTH - 100, 10))

    # Update and draw all game objects
    for entity in all_sprites:
        if isinstance(entity, (Player, Enemy)):
            entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    # Handle coin collection
    collected_coins = pygame.sprite.spritecollide(P1, coins, True)
    COIN_COUNT += len(collected_coins)
    # Respawn new coins for collected ones
    for _ in collected_coins:
        new_coin = Coin()
        coins.add(new_coin)
        all_sprites.add(new_coin)

    # Check for collisions with enemies
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('images for racer/crash.wav').play()
        time.sleep(1)
        
        # Show game over screen
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over_text, (30, 250))
        pygame.display.update()
        
        # Cleanup and exit
        for entity in all_sprites:
            entity.kill() 
        time.sleep(2)
        pygame.quit()
        sys.exit()        
    
    # Update display and maintain FPS
    pygame.display.update()
    FramePerSec.tick(FPS)