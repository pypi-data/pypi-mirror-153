import pygame
from pygame.sprite import Sprite
import random

class Food(Sprite):
    def __init__(self, pos, screen, width):
        pygame.sprite.Sprite.__init__(self)
        self.position = pos
        self.width = width
        self.screen = screen

    def draw(self):
        # self.position = [random.randrange(0, 500-size), random.randrange(0, 500-size)]
        pygame.draw.rect(self.screen, (255,255,255),
        pygame.Rect(int(self.position[0]), int(self.position[1]), self.width, self.width))
