import pygame
import random
import psycopg2
import sys

#подключение к базуданных
DB_PARAMS = {
    "dbname": "snake_db",
    "user": "postgres",
    "password": "12345678",
    "host": "localhost",
}

try:
    conn = psycopg2.connect(**DB_PARAMS)
except psycopg2.Error as e:
    print("Невозможно подключиться к базе данных:", e)
    sys.exit(1)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username VARCHAR(50) PRIMARY KEY,
        level INTEGER
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_scores (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50),
        score INTEGER,
        level INTEGER,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()
#создание игрока
def get_or_create_user(username):
    cursor.execute("SELECT level FROM users WHERE username = %s", (username,))
    row = cursor.fetchone()
    if row:
        print(f"С возвращением, {username}! Ваш текущий уровень: {row[0]}.")
        return row[0]
    else:
        cursor.execute("INSERT INTO users (username, level) VALUES (%s, %s)", (username, 1))
        conn.commit()
        print(f"Добро пожаловать, {username}! Начинаем игру с уровня 1.")
        return 1
#сохранение
def save_state(username, score, level):
    cursor.execute("INSERT INTO user_scores (username, score, level) VALUES (%s, %s, %s)",
                   (username, score, level))
    cursor.execute("UPDATE users SET level = %s WHERE username = %s", (level, username))
    conn.commit()
    print("Состояние игры сохранено.")

#данные
pygame.init()
WINDOW_SIZE = 600
CELL_DIMENSION = 30
BASE_FPS = 5

GRID_LIGHT = (173, 216, 230)
GRID_DARK = (25, 25, 112)
SNAKE_HEAD = (255, 0, 0)
SNAKE_BODY = (0, 128, 0)
FOOD_COLOR = (255, 215, 0)
TEXT_COLOR = (255, 200, 125)
GAME_OVER_BG = (255, 200, 200)
WALL_COLOR = (105, 105, 105)

display_surface = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Enhanced Snake Game")
clock = pygame.time.Clock()
game_font = pygame.font.Font(None, 36)

#экран ввода
def username_input_screen():
    input_box = pygame.Rect(WINDOW_SIZE // 2 - 150, WINDOW_SIZE // 2 - 20, 300, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    username = ""
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if username.strip() != "":
                            done = True
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode

        display_surface.fill((0, 0, 0))
        prompt_text = game_font.render("Введите ваш юзернейм:", True, TEXT_COLOR)
        display_surface.blit(prompt_text, (WINDOW_SIZE // 2 - prompt_text.get_width() // 2, WINDOW_SIZE // 2 - 80))

        txt_surface = game_font.render(username, True, color)
        width = max(300, txt_surface.get_width() + 10)
        input_box.w = width
        display_surface.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(display_surface, color, input_box, 2)
        
        pygame.display.flip()
        clock.tick(30)
    return username

#классы
class GridPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Snake:
    def __init__(self):
        self.segments = [GridPoint(10, 11), GridPoint(10, 12), GridPoint(10, 13)]
        self.direction = GridPoint(1, 0)
        
    def update_position(self, walls, level):
        new_head = GridPoint(
            self.segments[0].x + self.direction.x,
            self.segments[0].y + self.direction.y
        )
        grid_size = WINDOW_SIZE // CELL_DIMENSION
        
        if level % 2 == 0:
            # Для четного уровня реализуем проход
            new_head.x %= grid_size
            new_head.y %= grid_size
        else:
            # Для нечетного уровня, если вышли за границы - конец игры
            if not (0 <= new_head.x < grid_size and 0 <= new_head.y < grid_size):
                return True

        # Проверка столкновения с самим собой
        if any(segment.x == new_head.x and segment.y == new_head.y for segment in self.segments):
            return True

        self.segments.insert(0, new_head)
        self.segments.pop()
        return False

    def add_segment(self):
        self.segments.append(GridPoint(self.segments[-1].x, self.segments[-1].y))

    def draw(self):
        pygame.draw.rect(display_surface, SNAKE_HEAD,
                         (self.segments[0].x * CELL_DIMENSION,
                          self.segments[0].y * CELL_DIMENSION,
                          CELL_DIMENSION, CELL_DIMENSION))
        for segment in self.segments[1:]:
            pygame.draw.rect(display_surface, SNAKE_BODY,
                             (segment.x * CELL_DIMENSION,
                              segment.y * CELL_DIMENSION,
                              CELL_DIMENSION, CELL_DIMENSION))

class Food:
    LIFETIME = 5000
    
    def __init__(self, snake):
        self.position = self.generate_position(snake)
        self.spawn_time = pygame.time.get_ticks()
        self.weight = random.choices([1, 2, 3], weights=[70, 25, 5])[0]
        
    def generate_position(self, snake):
        while True:
            new_pos = GridPoint(
                random.randint(0, (WINDOW_SIZE // CELL_DIMENSION) - 1),
                random.randint(0, (WINDOW_SIZE // CELL_DIMENSION) - 1)
            )
            if not any(segment.x == new_pos.x and segment.y == new_pos.y for segment in snake.segments):
                return new_pos

    def draw(self):
        colors = {1: (0, 255, 0), 2: (255, 255, 0), 3: (255, 0, 0)}
        pygame.draw.rect(display_surface, colors[self.weight],
                         (self.position.x * CELL_DIMENSION,
                          self.position.y * CELL_DIMENSION,
                          CELL_DIMENSION, CELL_DIMENSION))

def create_game_grid():
    for row in range(WINDOW_SIZE // CELL_DIMENSION):
        for col in range(WINDOW_SIZE // CELL_DIMENSION):
            cell_color = GRID_LIGHT if (row + col) % 2 == 0 else GRID_DARK
            pygame.draw.rect(display_surface, cell_color,
                             (col * CELL_DIMENSION, row * CELL_DIMENSION,
                              CELL_DIMENSION, CELL_DIMENSION))
#пауза и сохранение
def pause_game(username, score, level):
    save_state(username, score, level)
    pause_text = game_font.render("Игра на паузе. Нажмите P для продолжения.", True, TEXT_COLOR)
    display_surface.blit(pause_text, (WINDOW_SIZE // 2 - pause_text.get_width() // 2, WINDOW_SIZE // 2))
    pygame.display.update()
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
        clock.tick(5)

def run_game(username, starting_level):
    current_speed = BASE_FPS + (starting_level - 1) * 2
    current_level = starting_level
    snake = Snake()
    food = Food(snake)
    player_score = 0
    is_game_over = False

    while not is_game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and snake.direction.x != -1:
                    snake.direction = GridPoint(1, 0)
                elif event.key == pygame.K_LEFT and snake.direction.x != 1:
                    snake.direction = GridPoint(-1, 0)
                elif event.key == pygame.K_DOWN and snake.direction.y != -1:
                    snake.direction = GridPoint(0, 1)
                elif event.key == pygame.K_UP and snake.direction.y != 1:
                    snake.direction = GridPoint(0, -1)
                elif event.key == pygame.K_p:
                    pause_game(username, player_score, current_level)

        if pygame.time.get_ticks() - food.spawn_time > Food.LIFETIME:
            food = Food(snake)
        is_game_over = snake.update_position([], current_level)
        if snake.segments[0].x == food.position.x and snake.segments[0].y == food.position.y:
            player_score += food.weight
            snake.add_segment()
            food = Food(snake)
            if player_score % 4 == 0:
                current_level += 1
                current_speed += 2

        create_game_grid()
        snake.draw()
        food.draw()
        score_label = game_font.render(f"Score: {player_score}  Level: {current_level}", True, TEXT_COLOR)
        display_surface.blit(score_label, (10, 10))
        pygame.display.update()
        clock.tick(current_speed)

    display_surface.fill(GAME_OVER_BG)
    final_score_text = game_font.render(f"Final Score: {player_score}", True, TEXT_COLOR)
    display_surface.blit(final_score_text, (WINDOW_SIZE // 2 - final_score_text.get_width() // 2, WINDOW_SIZE // 2))
    pygame.display.update()
    pygame.time.wait(3000)
    save_state(username, player_score, current_level)

#запуск
if __name__ == "__main__":
    username = username_input_screen()
    starting_level = get_or_create_user(username)
    run_game(username, starting_level)
    cursor.close()
    conn.close()
    pygame.quit()
