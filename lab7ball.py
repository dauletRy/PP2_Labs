import pygame

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Movable Ball")

WHITE = (255, 255, 255)
RED = (255, 0, 0)

radius = 25
x, y = width // 2, height // 2

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            new_x, new_y = x, y
            
            if event.key == pygame.K_UP:
                new_y -= 20
            elif event.key == pygame.K_DOWN:
                new_y += 20
            elif event.key == pygame.K_LEFT:
                new_x -= 20
            elif event.key == pygame.K_RIGHT:
                new_x += 20
            
            x = max(radius, min(new_x, width - radius))
            y = max(radius, min(new_y, height - radius))

    screen.fill(WHITE)
    pygame.draw.circle(screen, RED, (x, y), radius)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()