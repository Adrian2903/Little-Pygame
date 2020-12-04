# from pygame import *
import pygame as pg
import os, sys
import itertools
import re
PATH = sys.path[0]

pg.init()
screen = pg.display.set_mode((700, 600))
FONT = pg.font.SysFont('Comic Sans MS', 32)
# Default button images/pygame.Surfaces.
IMAGE_NORMAL = pg.Surface((100, 32))
IMAGE_NORMAL.fill((40, 40, 40))
IMAGE_HOVER = [pg.image.load(os.path.join(PATH, "red.png")), pg.image.load(os.path.join(PATH, "yellow.png"))]
IMAGE_DOWN = pg.Surface((100, 32))
IMAGE_DOWN.fill(pg.Color('aquamarine1'))


# Button is a sprite subclass, that means it can be added to a sprite group.
# You can draw and update all sprites in a group by
# calling `group.update()` and `group.draw(screen)`.
class Button(pg.sprite.Sprite):

    def __init__(self, x, y, width, height, callback,
                 font=FONT, text='', text_color=(0, 0, 0),
                 image_normal=IMAGE_NORMAL, image_hover=IMAGE_HOVER,
                 image_down=IMAGE_DOWN):
        super().__init__()
        self.active = True
        # Scale the images to the desired size (doesn't modify the originals).
        self.image_normal = pg.transform.scale(image_normal, (width, height))
        self.image_hover = pg.transform.scale(image_hover[0], (width, height))
        self.image_hover1 = pg.transform.scale(image_hover[1], (width, height))
        self.image_down = pg.transform.scale(image_down, (width, height))

        self.image = self.image_normal  # The currently active image.
        self.rect = self.image.get_rect(topleft=(x, y))
        # To center the text rect.
        self.image_center = self.image.get_rect().center
        text_surf = font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=self.image_center)
        # Blit the text onto the images.
        for image in (self.image_normal, self.image_hover, self.image_down):
            image.blit(text_surf, text_rect)

        # This function will be called when the button gets pressed.
        self.callback = callback
        self.button_down = False

    def handle_event(self, event, turn):
        if event.type == pg.MOUSEBUTTONDOWN and self.active:
            if self.rect.collidepoint(event.pos):
                # self.image = self.image_down
                self.button_down = True
        elif event.type == pg.MOUSEBUTTONUP and self.active:
            # If the rect collides with the mouse pos.
            if self.rect.collidepoint(event.pos) and self.button_down:
                if turn == "0":
                    self.callback(pg.mouse.get_pos()[0]//100, self.image_hover)  # Call the function.
                else:
                    self.callback(pg.mouse.get_pos()[0]//100, self.image_hover1)  # Call the function.
            if self.active:
                self.image = self.image_normal
            self.button_down = False
        elif event.type == pg.MOUSEMOTION and self.active:
            collided = self.rect.collidepoint(event.pos)
            if collided and not self.button_down:
                if turn == "0":
                    self.image = self.image_hover
                else:
                    self.image = self.image_hover1
            elif not collided:
                self.image = self.image_normal


class Game:

    def __init__(self, screen):
        self.TURN = itertools.cycle("01")
        self.PATTERNS = [re.compile(pattern) for pattern in map(r"([01])(.{{{}}}\1){{3}}".format, (0, 5, 6, 7))]
        self.done = False
        self.clock = pg.time.Clock()
        self.screen = screen
        self.turn = next(self.TURN)
        # Contains all sprites. Also put the button sprites into a
        # separate group in your own game.
        self.all_sprites = [pg.sprite.Group(), pg.sprite.Group(), pg.sprite.Group(), pg.sprite.Group(), pg.sprite.Group(), pg.sprite.Group(), pg.sprite.Group()]
        self.number = 0
        self.pos = [5, 5, 5, 5, 5, 5, 5]
        self.board = [""] * 7
        # Create the button instances. You can pass your own images here.
        for x in range(0, 601, 100):
            for y in range(0, 501, 100):
                self.all_sprites[x//100].add(
                    Button(
                        x, y, 100, 100, self.change,
                        FONT, "", (255, 255, 255),
                        IMAGE_NORMAL, IMAGE_HOVER, IMAGE_DOWN)
                )

    def check(self):
        board_state = '_'.join(row.ljust(6) for row in self.board)
        return any(pattern.search(board_state) for pattern in self.PATTERNS)

    def change(self, x, img):
        for index, btn in enumerate(self.all_sprites[x]):
            if index == self.pos[x]:
                self.board[x] += self.turn
                btn.image = img
                btn.active = False
                self.pos[x] -= 1
                self.turn = next(self.TURN)
                if self.check():
                    self.done = True

    def run(self):
        while not self.done:
            self.dt = self.clock.tick(30) / 1000
            self.handle_events()
            self.run_logic()
            if self.check():
                for buttons in self.all_sprites:
                    for button in buttons:
                        button.active = False
            self.draw()
        self.play_again()

    def play_again(self):
        done = True
        while done:
            if self.check():
                winner = "Red" if self.turn == "1" else "Yellow"
                msg = FONT.render(f"{winner} won!!", True, (255, 255, 255))
                text_rect = msg.get_rect(center=(350, 300))
                screen.blit(msg, text_rect)
                pg.display.update()
            else:
                break
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = False

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            for buttons in self.all_sprites:
                for button in buttons:
                    button.handle_event(event, self.turn)

    def run_logic(self):
        for buttons in self.all_sprites:
            buttons.update(self.dt)

    def draw(self):
        self.screen.fill((30, 30, 30))
        for buttons in self.all_sprites:
            buttons.draw(self.screen)
        for x in range(0, 701, 100):
            pg.draw.line(self.screen, (0, 0, 0), (x, 0), (x, 600))
            for y in range(0, 601, 100):
                pg.draw.line(self.screen, (0, 0, 0), (x, y), (700, y))

        pg.display.flip()


if __name__ == '__main__':
    pg.init()
    Game(screen).run()
    pg.quit()