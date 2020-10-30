import pygame
import time
import random

# init
pygame.init()

# display
dis_width, dis_height = 800, 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption("Snake Game")

# color
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 102)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# clock
clock = pygame.time.Clock()

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def your_score(score):
    value = score_font.render("Your Score: " + str(score), True, YELLOW)
    dis.blit(value, [0, 0])

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, RED, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width//6, dis_height//3])

def hs(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width//6, dis_height//3 + 20])

def game_loop():
    # initial state
    game_over = False
    game_close = False
    direction = ""

    # snake
    snake_block = 10
    snake_speed = 15
    
    # pos
    x1, y1 = dis_width//2, dis_height//2
    x1_change, y1_change = 0, 0

    # our snake
    snake_list = []
    snake_length = 1

    # food
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    # game loop
    while not game_over:

        # game over
        while game_close:
            dis.fill(BLACK)
            your_score(snake_length-1)

            f = open("E:\Lang\Belajar Python\Little-Pygame\Snake\highscore.txt", "r")
            score = f.read()
            score = max(int(score), snake_length-1)
            f.close()

            f = open("E:\Lang\Belajar Python\Little-Pygame\Snake\highscore.txt", "w")
            f.write(str(score))
            f.close()
            message("You Lost! Press Q-Quit or C-Play Again", RED)
            hs(f"Highscore: {score}", RED)
            
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    elif event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            
            # key press (arrow)
            if event.type == pygame.KEYDOWN and snake_length > 1:
                if event.key == pygame.K_LEFT and direction is not "right":
                    x1_change = -snake_block
                    y1_change = 0
                    direction = "left"
                elif event.key == pygame.K_RIGHT and direction is not "left":
                    x1_change = snake_block
                    y1_change = 0
                    direction = "right"
                elif event.key == pygame.K_UP and direction is not "down":
                    x1_change = 0
                    y1_change = -snake_block
                    direction = "up"
                elif event.key == pygame.K_DOWN and direction is not "up":
                    x1_change = 0
                    y1_change = snake_block
                    direction = "down"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                    direction = "left"
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                    direction = "right"
                elif event.key == pygame.K_UP:
                    x1_change = 0
                    y1_change = -snake_block
                    direction = "up"
                elif event.key == pygame.K_DOWN:
                    x1_change = 0
                    y1_change = snake_block
                    direction = "down"
        
        # wall limit
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        
        # update pos
        x1 += x1_change
        y1 += y1_change
        
        # background color 
        dis.fill(BLACK)
        
        # draw snake and food
        pygame.draw.rect(dis, GREEN, [foodx, foody, snake_block, snake_block])
        pygame.display.update()

        snake_head = [x1, y1]
        snake_list.append(snake_head)

        # keep the length of snake
        if len(snake_list) > snake_length:
            del snake_list[0]

        # crash own body
        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        our_snake(snake_block, snake_list)
        your_score(snake_length-1)
        pygame.display.update()

        if (x1, y1) == (foodx, foody):
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            snake_length += 1

        snake_speed = min(25, snake_speed + snake_length//5)

        clock.tick(snake_speed)

    pygame.quit()
    quit()

game_loop()