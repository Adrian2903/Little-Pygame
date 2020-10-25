# from pygame import *
import pygame
import sys

# setting global variable
XO = "X"
winner = None
draw = False
board = [[None] * 3] * 3

pygame.init()

width = 450
height = 450
fps = 30
CLOCK = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

screen = pygame.display.set_mode((width, height+100))
pygame.display.set_caption("Tic Tac Toe")
pygame.display.update()

cross_font = pygame.font.SysFont("bahnschrift", 200)
font_style = pygame.font.SysFont("comicsansms", 30)

def status():
    global draw

    if winner is None:
        msg = XO + "'s Turn"
    else:
        msg = "X Win!" if XO == "O" else "O Win!"
    if draw:
        msg = "Game Draw!"

    msg = font_style.render(msg, True, WHITE)
    screen.fill(BLACK, (0, width, height, 100))
    text_rect = msg.get_rect(center = (width/2, height+50))
    screen.blit(msg, text_rect)
    pygame.display.update()

def game_start():
    global XO, winner, board, draw

    XO = "X"
    winner = None
    board = [[None] * 3, [None] * 3, [None] * 3]
    draw = False

    screen.fill(WHITE)

    pygame.draw.line(screen, BLACK, (0, height//3), (600, height//3), 4)
    pygame.draw.line(screen, BLACK, (0, height//3*2), (600, height//3*2), 4)
    pygame.draw.line(screen, BLACK, (width//3, 0), (width//3, 600), 4)
    pygame.draw.line(screen, BLACK, (width//3*2, 0), (width//3*2, 600), 4)
    status()

def check_win():
    global board, winner, draw

    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
            winner = board[row][0]
            pygame.draw.line(screen, RED, (0, (row+1)*height//3 - height//6), (width, (row+1)*height//3 - height//6), 4)
            break
    
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            winner = board[0][col]
            pygame.draw.line(screen, RED, ((col+1)*width//3 - width//6, 0), ((col+1)*width//3 - width//6, height), 4)
            break
    
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        winner = board[0][0]
        pygame.draw.line(screen, RED, (0, 0), (width, height), 4)

    if board[0][2] == board[1][1] == board[2][0] and board[1][1] is not None:
        winner = board[0][2]
        pygame.draw.line(screen, RED, (width, 0), (0, height), 4)
    
    if all(all(row) for row in board) and winner is None:
        draw = True
    status()

def drawXO(row, col):
    global board, XO

    if row == 1:
        pos_y = 0
    elif row == 2:
        pos_y = width//3
    else:
        pos_y = width//3*2

    if col == 1:
        pos_x = 0
    elif col == 2:
        pos_x = height//3
    else:
        pos_x = height//3*2

    board[row-1][col-1] = XO
    value = cross_font.render(XO, True, BLACK)
    if XO == "X":
        screen.blit(value, [pos_x+29, pos_y+16])
        XO = "O"
    elif XO == "O":
        screen.blit(value, [pos_x+21, pos_y+16])
        XO = "X"
    pygame.display.update()

def user_click():
    x, y = pygame.mouse.get_pos()

    if x < width//3:
        col = 1
    elif x < width//3*2:
        col = 2
    elif x < width:
        col = 3
    else:
        col = None

    if y < height//3:
        row = 1
    elif y < height//3*2:
        row = 2
    elif y < height:
        row = 3
    else:
        row = None

    if row and col and board[row-1][col-1] is None:
        global XO

        drawXO(row, col)
        check_win()

def reset_game():
    global XO, board, winner, draw
    
    XO = "X"
    draw = False
    winner = None
    board = [[None] * 3, [None] * 3, [None] * 3]

    game_start()

def message(msg):
    msg = font_style.render(msg, True, RED)
    screen.blit(msg, (width//2-140, height//2-20))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_p:
                    return

game_start()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            user_click()
            if winner or draw:
                message("Press Q-quit or P-play")
                reset_game()
    
    pygame.display.update()
    CLOCK.tick(fps)