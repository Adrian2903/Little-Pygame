import pygame
from string import ascii_uppercase as up
import math
import os, sys
import word_list

game_dir = sys.path[0]

# window size
WIDTH, HEIGHT = 800, 500

# color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")

def main():
    images = []
    for i in range(8):
        image = pygame.image.load(os.path.join(game_dir, f"hangman{i}.png"))
        images.append(image)

    # setup game loop
    FPS = 60
    clock = pygame.time.Clock()
    run = True
    hangman_status = 0
    word = word_list.pokemon().upper()
    correct_guess = []
    win = False

    # button and text
    RADIUS = 20
    GAP = 15
    font = pygame.font.SysFont("imprintshadow", 20)
    font2 = pygame.font.SysFont("imprintshadow", 40)
    letters = []
    startx = round((WIDTH - (2 * RADIUS + GAP) * 12 - 2 * RADIUS)/2)
    starty = 400
    for i in range(26):
        x = startx + RADIUS + (RADIUS * 2 + GAP) * (i % 13)
        y = starty + i // 13 * (GAP + RADIUS * 2)
        letters.append([x, y, up[i], BLACK])

    def draw():
        screen.fill(WHITE)

        # draw guess
        display_word = ""
        for ltr in word:
            if not ltr.isalpha():
                display_word += ltr + " "
            elif ltr in correct_guess:
                display_word += ltr + " "
            else:
                display_word += "_ "
        text = font2.render(display_word, True, BLACK)
        text_rect = text.get_rect(center = (540, 200))
        screen.blit(text, text_rect)

        for letter in letters:
            x, y, z, c = letter
            z = font.render(z, True, BLACK)
            pygame.draw.circle(screen, BLACK, (x, y), RADIUS, 3)
            if c == GREEN:
                pygame.draw.circle(screen, GREEN, (x, y), RADIUS-3, RADIUS-3)
            elif c == RED:
                pygame.draw.circle(screen, RED, (x, y), RADIUS-3, RADIUS-3)
            screen.blit(z, (x - z.get_width()//2, y - z.get_height()//2))

        screen.blit(images[hangman_status % 8], (120, 60))

        pygame.display.update()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                ltr = event.key
                ltr -= 32
                if 65 <= ltr <= 90:
                    ltr = chr(ltr)
                    if ltr in word and letters[up.index(ltr)][3] == BLACK:
                        letters[up.index(ltr)][3] = GREEN
                        correct_guess.append(ltr)
                        if len(correct_guess) == len(set(word)):
                            run = False
                            win = True
                        break
                    elif ltr not in word and letters[up.index(ltr)][3] == BLACK:
                        letters[up.index(ltr)][3] = RED
                        hangman_status += 1
                        if hangman_status > 6:
                            run = False
                        break
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for i, j in enumerate(letters):
                    x, y, z, c = j
                    dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                    if dis <= RADIUS:
                        if z in word and c == BLACK:
                            letters[i][3] = GREEN
                            correct_guess.append(z)
                            if len(correct_guess) == len(set(word)):
                                run = False
                                win = True
                            break
                        elif z not in word and c == BLACK:
                            letters[i][3] = RED
                            hangman_status += 1
                            if hangman_status > 6:
                                run = False
                            break
        
        draw()

    run = True
    while run:
        for event in pygame.event.get():
            msg = "Play Again? Y/N"
            text = font2.render(msg, True, RED)
            text_rect = text.get_rect(center = (400, 280))
            screen.blit(text, text_rect)
            if win:
                text2 = font2.render("YAY!!!", True, GREEN)
                text_rect2 = text2.get_rect(center = (400, 240))
                screen.blit(text2, text_rect2)
            else:
                text2 = font2.render("Correct Answer: " + word, True, RED)
                text_rect2 = text2.get_rect(center = (400, 240))
                screen.blit(text2, text_rect2)

            pygame.display.update()
            
            if event.type == pygame.QUIT:
                run = False
                break
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    run = False
                    break
                elif event.key == pygame.K_y:
                    run = False
                    main()

main()
pygame.quit()