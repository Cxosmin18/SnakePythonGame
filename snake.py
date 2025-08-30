import pygame
import sys
import random

pygame.init()
pygame.mixer.init()

width, height = 600, 400
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sarpe joc")

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (160, 32, 240)
GRAY = (100, 100, 100)

snake_size = 10
base_speed = snake_size
font = pygame.font.SysFont("Arial", 24)

# Sunete
eat_sound = pygame.mixer.Sound("eat.wav")
boost_sound = pygame.mixer.Sound("animeWow.wav")
game_over_sound = pygame.mixer.Sound("gameOver2.mp3")

clock = pygame.time.Clock()

def draw_button(text, x, y, w, h):
    pygame.draw.rect(window, GRAY, (x, y, w, h))
    label = font.render(text, True, WHITE)
    label_rect = label.get_rect(center=(x + w // 2, y + h // 2))
    window.blit(label, label_rect)

def show_start_screen():
    pygame.mixer.music.load("muzicaDeStart.wav")
    pygame.mixer.music.play(-1)
    while True:
        window.fill(BLACK)
        draw_button("Start", width // 2 - 50, height // 2 - 25, 100, 50)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if width // 2 - 50 <= mx <= width // 2 + 50 and height // 2 - 25 <= my <= height // 2 + 25:
                    pygame.mixer.music.stop()
                    return

def show_game_over(score):
    while True:
        window.fill(BLACK)
        game_over_text = font.render(f"Oops! - Scor final: {score}", True, WHITE)
        restart_text = font.render("Click pe Restart pentru a reîncepe", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(width // 2, height // 2 - 60))
        restart_rect = restart_text.get_rect(center=(width // 2, height // 2 - 30))
        window.blit(game_over_text, game_over_rect)
        window.blit(restart_text, restart_rect)
        draw_button("Restart", width // 2 - 50, height // 2 + 20, 100, 50)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if width // 2 - 50 <= mx <= width // 2 + 50 and height // 2 + 20 <= my <= height // 2 + 70:
                    return

def spawn_food():
    food_type = random.choices(["white", "yellow", "purple"], weights=[5, 2, 3])[0]
    pos = [random.randrange(0, width, snake_size), random.randrange(0, height, snake_size)]
    if food_type == "white":
        return pos, WHITE, "white"
    elif food_type == "yellow":
        return pos, YELLOW, "yellow"
    else:
        return pos, PURPLE, "purple"

def start_game():
    pygame.mixer.music.load("muzicaInJoc.wav")
    pygame.mixer.music.play(-1)

    snake_pos = [[100, 50], [90, 50], [80, 50]]
    direction = 'RIGHT'
    score = 0
    grow_by = 0
    speed = base_speed
    boost_timer = 0

    food_pos, food_color, food_type = spawn_food()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and direction != 'DOWN':
                    direction = 'UP'
                elif event.key == pygame.K_s and direction != 'UP':
                    direction = 'DOWN'
                elif event.key == pygame.K_a and direction != 'RIGHT':
                    direction = 'LEFT'
                elif event.key == pygame.K_d and direction != 'LEFT':
                    direction = 'RIGHT'

        head_x, head_y = snake_pos[0]
        if direction == 'RIGHT':
            new_head = [head_x + speed, head_y]
        elif direction == 'LEFT':
            new_head = [head_x - speed, head_y]
        elif direction == 'UP':
            new_head = [head_x, head_y - speed]
        elif direction == 'DOWN':
            new_head = [head_x, head_y + speed]

        snake_pos.insert(0, new_head)

        # Coliziune cu corpul
        if new_head in snake_pos[1:]:
            pygame.mixer.music.stop()
            game_over_sound.play()
            show_game_over(score)
            return

        # Coliziune cu mancarea
        if abs(new_head[0] - food_pos[0]) < snake_size and abs(new_head[1] - food_pos[1]) < snake_size:
            if food_type == "white":
                score += 5
                grow_by += 3
                eat_sound.play()
            elif food_type == "yellow":
                score += 10
                grow_by += 5
                eat_sound.play()
            elif food_type == "purple":
                score += 50
                grow_by += 8
                boost_sound.play()
                speed = base_speed * 2
                boost_timer = pygame.time.get_ticks() + 2000
            food_pos, food_color, food_type = spawn_food()
        else:
            if grow_by > 0:
                grow_by -= 1
            else:
                snake_pos.pop()

        # Reset boost dupa 2 secunde
        if boost_timer and pygame.time.get_ticks() > boost_timer:
            speed = base_speed
            boost_timer = 0

        # Wrap la margini
        for segment in snake_pos:
            if segment[0] >= width:
                segment[0] = 0
            elif segment[0] < 0:
                segment[0] = width - snake_size
            if segment[1] >= height:
                segment[1] = 0
            elif segment[1] < 0:
                segment[1] = height - snake_size

        window.fill(BLACK)

        # Deseneaza sarpele
        for pos in snake_pos:
            pygame.draw.rect(window, GREEN, pygame.Rect(pos[0], pos[1], snake_size, snake_size))

        # Deseneaza mancarea
        pygame.draw.rect(window, food_color, pygame.Rect(food_pos[0], food_pos[1], snake_size, snake_size))

        # Scorul
        score_text = font.render(f"Scor: {score}", True, WHITE)
        window.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(15)

while True:
    show_start_screen()
    start_game()
