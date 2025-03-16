import pygame
import datetime

pygame.init()

width, height = 1000, 1000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Mickey Clock")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

try:
    minute_hand = pygame.image.load("images for clock/images/rightarm.png").convert_alpha()
    second_hand = pygame.image.load("images for clock/images/leftarm.png").convert_alpha()
    background = pygame.image.load("images for clock/images/clock.png").convert()
except pygame.error as e:
    print(f"Error loading images: {e}")
    pygame.quit()
    exit()

bg_rect = background.get_rect(center=(width//2, height//2))
font = pygame.font.SysFont('Arial', 36, bold=True)

def get_time():
    now = datetime.datetime.now().time()
    return {
        'h': now.hour % 12,
        'm': now.minute,
        's': now.second
    }

def rotate(image, angle, pivot):
    rotated_image = pygame.transform.rotate(image, angle)
    return rotated_image, rotated_image.get_rect(center=pivot)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    t = get_time()
    rotated_minute, minute_rect = rotate(minute_hand, -(t['m'] * 6), bg_rect.center)
    rotated_second, second_rect = rotate(second_hand, -(t['s'] * 6), bg_rect.center)

    screen.fill(WHITE)
    screen.blit(background, bg_rect)
    screen.blit(rotated_minute, minute_rect)
    screen.blit(rotated_second, second_rect)
    pygame.draw.circle(screen, BLACK, bg_rect.center, 10)

    time_text = font.render(f"{t['h']:02}:{t['m']:02}:{t['s']:02}", True, BLACK)
    screen.blit(time_text, time_text.get_rect(center=(width//2, height-50)))
    
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()