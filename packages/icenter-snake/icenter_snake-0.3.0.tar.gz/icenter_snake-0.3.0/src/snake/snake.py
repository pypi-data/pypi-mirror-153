import pygame
from pygame.sprite import Sprite
import random

class Snake():

    def __init__(self, dir, pos_list, length, width, screen):
        self.COLOR = (0,0,255)
        # print('hi')
        pygame.sprite.Sprite.__init__(self)
        self.direction = dir
        self.pos_list = pos_list
        self.length = length
        self.width = width
        self.screen = screen
        self.last_tail_position = [0,0]

    def move(self):
        # snake_len = 3 # to change later

        # for i in range (snake_len):
            # self.position[i] += self.speed[i]
        head_pos = [-1, -1]
        self.last_tail_position = self.pos_list[-1]
        if self.direction == 0:
            head_pos[0] = self.pos_list[0][0]
            head_pos[1] = self.pos_list[0][1] - self.width
        if self.direction == 1:
            head_pos[0] = self.pos_list[0][0]
            head_pos[1]= self.pos_list[0][1] + self.width
        if self.direction == 2:
            head_pos[0] = self.pos_list[0][0] - self.width
            head_pos[1] = self.pos_list[0][1]
        if self.direction == 3:
            head_pos[0] = self.pos_list[0][0] + self.width
            head_pos[1] = self.pos_list[0][1]
        self.pos_list.insert(0, head_pos)
        del self.pos_list[-1]

    def eat(self):
        self.pos_list.append(self.last_tail_position)
        self.length += 1

    # def draw(self):
    #     pygame.draw.rect(self.screen, self.COLOR, pygame.rect(pos, pos, self.width, self.width))
