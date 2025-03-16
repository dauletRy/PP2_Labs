import pygame
import os

pygame.init()

width, height = 600, 400

screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("Music Player")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font = pygame.font.SysFont('Arial', 24)

music_dir = "C:/Users/daule/Desktop/work/pp2/music"
music_files = [f for f in os.listdir(music_dir) if f.endswith(('.mp3', '.wav', '.ogg'))]
music_files.sort()
current_track = 0

pygame.mixer.init()
pygame.mixer.music.load(os.path.join(music_dir, music_files[current_track]))

is_playing = False

controls = {
    pygame.K_SPACE: 'play/pause',
    pygame.K_ESCAPE: 'stop',
    pygame.K_RIGHT: 'next',
    pygame.K_LEFT: 'previous'
}

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in controls:
                action = controls[event.key]
                if action == 'play/pause':
                    if is_playing:
                        pygame.mixer.music.pause()
                        is_playing = False
                    else:
                        if pygame.mixer.music.get_busy():
                            pygame.mixer.music.unpause()
                        else:
                            pygame.mixer.music.play()
                        is_playing = True
                elif action == 'stop':
                    pygame.mixer.music.stop()
                    is_playing = False
                elif action == 'next':
                    current_track = (current_track + 1) % len(music_files)
                    pygame.mixer.music.load(os.path.join(music_dir, music_files[current_track]))
                    if is_playing:
                        pygame.mixer.music.play()
                elif action == 'previous':
                    current_track = (current_track - 1) % len(music_files)
                    pygame.mixer.music.load(os.path.join(music_dir, music_files[current_track]))
                    if is_playing:
                        pygame.mixer.music.play()

    screen.fill(WHITE)

    track_text = font.render(f"Now Playing: {music_files[current_track]}", True, BLACK)

    screen.blit(track_text, (20, 20))

    controls_text = font.render("SPACE: Play/Pause | LEFT/RIGHT: Previous/Next | ESC: Stop", True, BLACK)

    screen.blit(controls_text, (20, height - 40))
    
    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()