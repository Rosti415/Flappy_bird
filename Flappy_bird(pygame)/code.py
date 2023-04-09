import sys

import pygame
from pygame.locals import *


WIDTH, HEIGHT = 900, 500
BIRD_WIDTH, BIRD_HEIGHT = 40, 25
START_X, START_Y = 35, 200
FPS = 60

BACKGROUND = pygame.transform.scale(
    pygame.image.load("background.jpg"), (WIDTH, HEIGHT)
)
BIRD = pygame.transform.scale(
    pygame.image.load("bird.png"), (BIRD_WIDTH, BIRD_HEIGHT)
)


class Background:
    def __init__(self, start_coordinates, image, size):
        self.start_x = start_coordinates[0]
        self.start_y = start_coordinates[1]
        self.rect = pygame.rect.Rect(*start_coordinates, *size)
        self.image = image

    def to_start(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y

    def set_coordinates(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def get_coordinates(self):
        return self.rect.x, self.rect.y

    def move(self, speed):
        self.rect.x -= speed

        if self.rect.x < self.start_x - WIDTH:
            self.set_coordinates(self.start_x, self.start_y)


class Wall(Background):
    def __init__(self, start_coordinates, image, size):
        super().__init__(start_coordinates, image, size)


class Bird:
    def __init__(self):
        self.rect = pygame.rect.Rect(START_X, START_Y, BIRD_WIDTH, BIRD_HEIGHT)
        self.image = BIRD

    def fall(self):
        self.rect.y += 3

    def jump(self):
        self.rect.y -= 60
        self.rect.x += 0

    def lose(self):
        self.rect.x = START_X
        self.rect.y = START_Y


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.backgrounds = [
            Background((0, 0), BACKGROUND, (WIDTH, HEIGHT)),
            Background((WIDTH, 0), BACKGROUND, (WIDTH, HEIGHT)),
        ]

        self.walls = [
            Wall((40, 285), None, (75, 135)),
            Wall((40, 0), None, (75, 185)),
            Wall((40 + WIDTH, 285), None, (75, 135)),
            Wall((40 + WIDTH, 0), None, (75, 185)),
            Wall((255, 335), None, (75, 85)),
            Wall((255, 0), None, (75, 245)),
            Wall((255 + WIDTH, 335), None, (75, 85)),
            Wall((255 + WIDTH, 0), None, (75, 245)),
            Wall((482, 335), None, (75, 85)),
            Wall((480, 0), None, (75, 245)),
            Wall((482 + WIDTH, 335), None, (75, 85)),
            Wall((480 + WIDTH, 0), None, (75, 245)),
            Wall((708, 215), None, (75, 210)),
            Wall((708, 0), None, (75, 108)),
            Wall((708 + WIDTH, 215), None, (75, 210)),
            Wall((708 + WIDTH, 0), None, (75, 108)),
        ]

        self.bird = Bird()

        pygame.display.set_caption("Flappy Bird")

    def run(self):
        while True:
            for background in self.backgrounds:
                background.move(5)
                self.screen.blit(background.image, background.get_coordinates())

            for wall in self.walls:
                wall.move(5)
                #pygame.draw.rect(self.screen, (0, 255, 0), wall.rect)

                if self.bird.rect.colliderect(wall.rect):
                    self.bird.rect.x = START_X
                    self.bird.rect.y = START_Y

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.bird.jump()

            self.bird.fall()

            self.screen.blit(self.bird.image, (self.bird.rect.x, self.bird.rect.y))

            if self.bird.rect.y > HEIGHT - BIRD_HEIGHT + 2:
                self.bird.lose()

            self.clock.tick(FPS)
            pygame.display.update()


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
