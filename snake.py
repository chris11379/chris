import pygame
import random
import os

pygame.init()

width, height = 600, 400
block_size = 20
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 35)

HIGHSCORE_FILE = "highscore.txt"
def load_high_score():
    if os.path.exists(HIGHSCORE_FILE):
        try:
            return int(open(HIGHSCORE_FILE).read().strip())
        except:
            return 0
    return 0
def save_high_score(value):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(value))

def show_message(msg, color):
    text = font.render(msg, True, color)
    screen.blit(text, [width / 10, height / 3])

def show_score(score, color, high=None):
    score_text = font.render(f"score: {score}", True, color)
    screen.blit(score_text, [10, 10])
    if high is not None:
        high_text = font.render(f"High: {high}", True, color)
        screen.blit(high_text,[10, 40])

def game_loop():
    x = width // 2
    y = height //2
    x_change = 0
    y_change = 0
    
    snake_list = []
    snake_length = 1

    score = 0
    high = load_high_score()

    food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
    food_y = round(random.randrange(0, height - block_size) / block_size) * block_size

    game_over = False
    game_close = False

    while not game_over:

        while game_close:
            screen.fill(black)
            show_message("Game Over! Press c to Restart Press Q to quit", red)
            show_score(score, red, high)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        if score > high:
                            high = score
                            save_high_score(high)
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        if score > high:
                            high = score
                            save_high_score(high)
                        return
                elif event.type == pygame.QUIT:
                    if score > high:
                        high = score
                        save_high_score(high)
                    game_over = True
                    game_close = False
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -block_size
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = block_size
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -block_size
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = block_size
                    x_change = 0
        
        x += x_change
        y += y_change
        
        if x <0 or x >= width or y < 0 or y >= height:
            game_close = True
        
        screen.fill(black)
        pygame.draw.rect(screen, red, [food_x, food_y, block_size, block_size])

        snake_head = [x, y]
        snake_list.append(snake_head)

        if len(snake_list) >snake_length:
            del snake_list[0]
        
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True
        
        for segment in snake_list:
            pygame.draw.rect(screen, green, (segment[0], segment[1], block_size, block_size))

        show_score(score, red)

        pygame.display.update()

        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
            food_y = round(random.randrange(0, height - block_size) / block_size) * block_size
            snake_length += 1
            score += 1

        clock.tick(10)
    pygame. quit()
    quit()
while True:
    game_loop()