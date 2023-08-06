import snake
from snake import Food, Snake
from enum import Enum

import random
import pygame

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


def run():

    NAME = input("Enter your name: ")
    pygame.init()
    pygame.font.init()
    FONT = pygame.font.SysFont('Corbel', 30)

    SCREEN_SIZE = 480
    EXTRA_SCREEN_SIZE = 540
    SCREEN = pygame.display.set_mode([SCREEN_SIZE, EXTRA_SCREEN_SIZE])
    WIDTH = SCREEN.get_width()
    HEIGHT = SCREEN.get_height()
    COLOR = (255, 255, 255)
    BLACK = (0,0,0)
    SNAKE_WIDTH = 12

    difficulty = 'easy'
    time_delay = 70

    title = True
    running = True
    size = SNAKE_WIDTH

    x = SCREEN_SIZE/2
    y = SCREEN_SIZE/2

    init_snake_position = [[x,y], [x,y+size], [x,y+2*size]]
    init_len = len(init_snake_position)
    snake_obj = Snake(dir = 0, pos_list = init_snake_position, length = init_len, width = size, screen = SCREEN)

    food_pos = [12*random.randint(0, SCREEN_SIZE/SNAKE_WIDTH-1), 12*random.randint(0, SCREEN_SIZE/SNAKE_WIDTH-1)]

    food_obj = Food(pos = food_pos, screen = SCREEN, width = size)

    def collide(x,y):
        if x == SCREEN_SIZE or y == SCREEN_SIZE or x == -SNAKE_WIDTH or y == -SNAKE_WIDTH:
            # print("Collide Wall")
            return True
        for block in snake_obj.pos_list[1:]:
            if block == snake_obj.pos_list[0]:
                # print("Collide Self")
                return True
        else:
            return False

    def food_collide(x, y, food_x, food_y):
        if x == food_x and y == food_y:
            # print("Eat Food")
            return True
        else:
            return False

    name_string = ''
    while running:
        if (title):
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    running=False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        difficulty = 'easy'
                        time_delay = 80
                    elif event.key == pygame.K_2:
                        difficulty = 'medium'
                        time_delay = 50
                    elif event.key == pygame.K_3:
                        difficulty = 'hard'
                        time_delay = 25
                    elif event.key == pygame.K_RETURN:
                        title = False
                        SCORE = 0
            SCREEN.fill(BLACK)
            WELCOME_TITLE = FONT.render("Welcome to Snake!", True, COLOR)
            SCREEN.blit(WELCOME_TITLE, (120, 60))
            EASY = FONT.render('Press 1: Easy', True, COLOR)
            SCREEN.blit(EASY, (120,120))
            MEDIUM = FONT.render('Press 2: Medium', True, COLOR)
            SCREEN.blit(MEDIUM, (120,180))
            HARD = FONT.render('Press 3: Hard', True, COLOR)
            SCREEN.blit(HARD, (120,240))
            CURR_DIFF = FONT.render("Current difficulty: " + difficulty, True, COLOR)
            SCREEN.blit(CURR_DIFF, (120, 360))
            PRESS_ENTER = FONT.render("Press enter to start!", True, COLOR)
            SCREEN.blit(PRESS_ENTER, (120, 420))
        else:
            pygame.time.delay(time_delay)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if snake_obj.direction != 3:
                            # print("Left")
                            snake_obj.direction = 2
                    elif event.key == pygame.K_RIGHT:
                        if snake_obj.direction!= 2:
                            # print("RIGHT")
                            snake_obj.direction = 3
                    elif event.key == pygame.K_UP:
                        if snake_obj.direction != 1:
                            # print("UP")
                            snake_obj.direction = 0
                    elif event.key == pygame.K_DOWN:
                        if snake_obj.direction != 0:
                            # print("DOWN")
                            snake_obj.direction = 1

            # Move snake after direction change
            snake_obj.move()

            # Check for wall/snake collisions
            running = not collide(snake_obj.pos_list[0][0], snake_obj.pos_list[0][1])
            if not running:
                print("You just lost!")

            # Check for food collisions
            if food_collide(snake_obj.pos_list[0][0], snake_obj.pos_list[0][1], food_pos[0], food_pos[1]):
                snake_obj.eat()
                SCORE += 1
                food_pos = [12*random.randint(0, SCREEN_SIZE/SNAKE_WIDTH-1), 12*random.randint(0, SCREEN_SIZE/SNAKE_WIDTH-1)]
                food_obj = Food(pos = food_pos, screen = SCREEN, width = size)
            else:
                pass

            # Update the screen
            SCREEN.fill(BLACK)
            pygame.draw.rect(SCREEN, (255,0,0), pygame.Rect(0, SCREEN_SIZE, SCREEN_SIZE, 60))
            SCORE_DISPLAY = FONT.render("Score: " + str(SCORE), True, COLOR)
            SCREEN.blit(SCORE_DISPLAY, (15, 495))

            # Draw snake and food
            for segment in snake_obj.pos_list:
                pygame.draw.rect(SCREEN, (255,255,0), pygame.Rect(segment[0], segment[1], SNAKE_WIDTH, SNAKE_WIDTH))
            food_obj.draw()

        # Update screen
        pygame.display.update()


    pygame.quit()


if __name__ == '__main__':
    run()
