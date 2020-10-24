# from pygame import *
import pygame

pygame.init()

WIDTH = 800
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower of Hanoi")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
colors = [RED, GREEN, BLUE, YELLOW, PURPLE]

TEXT_FONT = pygame.font.SysFont("comicsans", 30)

xs = [140, 400, 660]
y = 30
index = 0
triangle = [[xs[index] - 10, y], [xs[index], y + 15], [xs[index] + 10, y]]

win = False

tmp_block = None
block_width = 220
block_height = 20
blocks0 = []
blocks1 = []
blocks2 = []
for i in range(5):
    blocks0.append([colors[i], 140 - block_width//2, HEIGHT - block_height * (i+1), block_width, block_height])
    block_width -= 40

def drop_block(index):
    global blocks0, blocks1, blocks2, tmp_block

    if index == 0:
        l = len(blocks0)
        if l == 0:
            blocks0.append(tmp_block)
            blocks0[0][2] = HEIGHT - block_height * (l + 1)
            tmp_block = None
        elif tmp_block[3] < blocks0[l-1][3]:
            blocks0.append(tmp_block)
            blocks0[l][2] = HEIGHT - block_height * (l + 1)
            tmp_block = None
        else:
            pass
    elif index == 1:
        l = len(blocks1)
        if l == 0:
            blocks1.append(tmp_block)
            blocks1[0][2] = HEIGHT - block_height * (l + 1)
            tmp_block = None
        elif tmp_block[3] < blocks1[l-1][3]:
            blocks1.append(tmp_block)
            blocks1[l][2] = HEIGHT - block_height * (l + 1)
            tmp_block = None
        else:
            pass
    elif index == 2:
        l = len(blocks2)
        if l == 0:
            blocks2.append(tmp_block)
            blocks2[0][2] = HEIGHT - block_height * (l + 1)
            tmp_block = None
        elif tmp_block[3] < blocks2[l-1][3]:
            blocks2.append(tmp_block)
            blocks2[l][2] = HEIGHT - block_height * (l + 1)
            tmp_block = None
        else:
            pass

    draw(tmp_block)

def take_block(index):
    global blocks0, blocks1, blocks2, tmp_block

    if index == 0 and len(blocks0) > 0:
        tmp_block = blocks0.pop()
    elif index == 1 and len(blocks1) > 0:
        tmp_block = blocks1.pop()
    elif index == 2 and len(blocks2) > 0:
        tmp_block = blocks2.pop()

    draw(tmp_block)

def draw(tmp_block):
    screen.fill(WHITE)

    pygame.draw.polygon(screen, BLACK, triangle)

    for i in range(3):
        pygame.draw.rect(screen, BLACK, (xs[i] - 10, 350, 20, 150))

    if tmp_block:
        pygame.draw.rect(screen, tmp_block[0], (tmp_block[1], 50, tmp_block[3], tmp_block[4]))

    for i in range(len(blocks0)):
        pygame.draw.rect(screen, blocks0[i][0], (blocks0[i][1], blocks0[i][2], blocks0[i][3], blocks0[i][4]))
    
    for i in range(len(blocks1)):
        pygame.draw.rect(screen, blocks1[i][0], (blocks1[i][1], blocks1[i][2], blocks1[i][3], blocks1[i][4]))
    
    for i in range(len(blocks2)):
        pygame.draw.rect(screen, blocks2[i][0], (blocks2[i][1], blocks2[i][2], blocks2[i][3], blocks2[i][4]))

    if win:
        msg = "You Win! Play Again? Y/N"
        text = TEXT_FONT.render(msg, True, GREEN)
        text_rect = text.get_rect(center = (400, 250))
        screen.blit(text, text_rect)
        pygame.display.update()

    pygame.display.update()

def main():
    global blocks0, blocks1, blocks2, tmp_block
    global xs, index, y
    global block_height, block_width
    global triangle, win

    xs = [140, 400, 660]
    y = 30
    index = 0
    win = False

    tmp_block = None
    block_width = 220
    block_height = 20
    blocks0 = []
    blocks1 = []
    blocks2 = []
    for i in range(5):
        blocks0.append([colors[i], 140 - block_width//2, HEIGHT - block_height * (i+1), block_width, block_height])
        block_width -= 40

    run = True
    while run:
        triangle = [[xs[index] - 10, y], [xs[index], y + 15], [xs[index] + 10, y]]
            
        draw(tmp_block)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    index = (index + 2) % 3
                    if tmp_block:
                        tmp_block[1] = xs[index] - tmp_block[3] // 2
                if event.key == pygame.K_RIGHT:
                    index = (index + 1) % 3
                    if tmp_block:
                        tmp_block[1] = xs[index] - tmp_block[3] // 2
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    if not tmp_block:
                        take_block(index)
                    else:
                        drop_block(index)
                if event.key == pygame.K_DOWN:
                    if tmp_block:
                        drop_block(index)

        if len(blocks2) == 5:
            run = False
            win = True

    while win:
        draw(tmp_block)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                win = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    win = False
                if event.key == pygame.K_y:
                    win = False
                    main()

main()
pygame.quit()