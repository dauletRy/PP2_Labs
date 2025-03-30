# Import necessary modules
import pygame, sys
from pygame.locals import *
import random, time

# Initialize Pygame and its mixer module
pygame.init()
pygame.mixer.init()

# Load and play background music
pygame.mixer.music.load("images for racer/background.wav")
pygame.mixer.music.set_volume(0.3)  # music vol
pygame.mixer.music.play(-1)  # infinity music loop

# Set up FPS (Frames Per Second) controller
FPS = 60
FramePerSec = pygame.time.Clock()

# Define color constants
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game configuration variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 3      # start speed
SCORE = 0      # players score
COIN_COUNT = 0 
SPEED_INCREASE_COIN = 5  # min coins for inc speed

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
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("images for racer/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.bottom > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # rand weight and percentage of spawning
        self.weight = random.choices([1, 2, 3], weights=[70, 25, 5])[0]
        
        # moneys graphics
        size = 20 + self.weight * 5  # size depends on weight
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # colors for different coins
        colors = {
            1: (255, 223, 0),   # gold
            2: (255, 144, 0), # orange
            3: (255, 0, 0)    # red
        }
        pygame.draw.circle(self.image, colors[self.weight], (size//2, size//2), size//2)
        self.rect = self.image.get_rect()
        self.respawn()

    def respawn(self):
        #random respawning of coin
        self.rect.topleft = (random.randint(0, SCREEN_WIDTH - self.rect.width),
                            random.randint(0, SCREEN_HEIGHT - self.rect.height))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("images for racer/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        self.speed = 5

    def move(self):
        #PLAYERS MOVEMENT
        pressed_keys = pygame.key.get_pressed()
        
        # horizontal
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        
        # vertical
        if self.rect.top > 0 and pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.speed + 2)
        if self.rect.bottom < SCREEN_HEIGHT and pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.speed - 2)

# initialization
P1 = Player()
E1 = Enemy()
coins = pygame.sprite.Group()

# starting money creating
for _ in range(3):
     coins.add(Coin())

# groups
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1)
all_sprites.add(*coins)


# main loop
while True:
    # event обработка
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # отрисовка
    DISPLAYSURF.blit(background, (0, 0))

    # visual
    score_surface = font_small.render(f"Score: {SCORE}", True, BLACK)
    coin_surface = font_small.render(f"Coins: {COIN_COUNT}", True, BLACK)
    DISPLAYSURF.blit(score_surface, (10, 10))
    DISPLAYSURF.blit(coin_surface, (SCREEN_WIDTH - 100, 10))

    # position updating
    for entity in all_sprites:
        if isinstance(entity, (Player, Enemy)):
            entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    # money сбор
    collected_coins = pygame.sprite.spritecollide(P1, coins, True)
    if collected_coins:
        # sum
        collected_weight = sum(coin.weight for coin in collected_coins)
        COIN_COUNT += collected_weight
        
        # speed inc
        prev_speed_level = (COIN_COUNT - collected_weight) // SPEED_INCREASE_COIN
        new_speed_level = COIN_COUNT // SPEED_INCREASE_COIN
        if new_speed_level > prev_speed_level:
            SPEED += 0.5 # inc
            
        # new money respawn
        for _ in collected_coins:
            new_coin = Coin()
            coins.add(new_coin)
            all_sprites.add(new_coin)

    # checking for столкновения
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('images for racer/crash.wav').play()
        time.sleep(1)
        
        # гейм овер
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over_text, (30, 250))
        pygame.display.update()
        
        # выход
        for entity in all_sprites:
            entity.kill() 
        time.sleep(2)
        pygame.quit()
        sys.exit()        
    
    # апдейт
    pygame.display.update()
    FramePerSec.tick(FPS)