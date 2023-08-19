import pygame as pg
import math
from math import sqrt
import random
import time

pg.init()
screen_width = 1600
screen_height = 1000
extra_height = 200
line_width = 6
font_obj = pg.font.Font('freesansbold.ttf', 64)
screen = pg.display.set_mode((screen_width, extra_height + screen_height), vsync=1)
target_radius = 30
pg.display.set_caption("Aim Trainer")

class Target:
    # constants
    START_SIZE = target_radius
    SHRINK_RATE = target_radius / 3000
    COLOR = 'red'
    DIFFERENT_COLOR = 'white'

    def __init__(self, x, y):
        # object
        self.size = self.START_SIZE
        self.shrink = True
        # coordinate
        self.x = x
        self.y = y

    def draw(self, screen):
        coordinate = (self.x, self.y)
        pg.draw.circle(screen, self.COLOR, coordinate, self.size)
        pg.draw.circle(screen, self.DIFFERENT_COLOR, coordinate, 0.6 * self.size)
        pg.draw.circle(screen, self.COLOR, coordinate, 0.36 * self.size)
        pg.draw.circle(screen, self.DIFFERENT_COLOR, coordinate, 0.216 * self.size)

    def update(self):
        if self.size - self.SHRINK_RATE <= 0:
            self.shrink = False

        if self.shrink == True:
            self.size -= self.SHRINK_RATE
        else:
            self.size = 0

def draw_targets(targets, screen):
    background = (200, 255, 255)
    screen.fill(background)

    for target in targets:
        target.draw(screen)

def main():
    print("\nClick on targets to increase your score")

    targets = []

    # solve board button
    score_button = pg.Rect(0, 0, 400, 100)
    score_surface = font_obj.render("Score:", True, (0, 0, 0))
    score_rect = score_surface.get_rect()
    score_rect.center = (200, 50) 
    # time "button"
    time_button = pg.Rect(400, 0, 600, 100)
    time_surface = font_obj.render("Time:", True, (0, 0, 0))
    time_rect = time_surface.get_rect()
    time_rect.center = (600, 50) 

    running = True
    score = 0
    while running:
        score_surface = font_obj.render("Score:"+str(score), True, (0, 0, 0))
        time = (pg.time.get_ticks() / 1000) // 1
        time_surface = font_obj.render("Time:"+str(time), True, (0, 0, 0))

        if len(targets) <= 3:
            rand_x = random.randint(0 + 2*target_radius, screen_width-1 - 2*target_radius)
            rand_y = random.randint(extra_height-1 + 2*target_radius, extra_height+screen_height-1 - 2*target_radius)
            target = Target(rand_x, rand_y)
            targets.append(target)
        
        for target in targets:
            target.update()
        draw_targets(targets, screen)

        pg.draw.rect(screen, (0,0,0), score_button, line_width)
        screen.blit(score_surface, score_rect)
        pg.draw.rect(screen, (0,0,0), time_button, line_width)
        screen.blit(time_surface, time_rect)

        pg.event.pump()
        mouse_down = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_down = True
            if event.type == pg.MOUSEBUTTONUP:
                mouse_down = False

        for target in targets:
            mouse_x = pg.mouse.get_pos()[0]
            mouse_y = pg.mouse.get_pos()[1]
            distance = sqrt((mouse_x - target.x)**2 + (mouse_y - target.y)**2)
            if distance < target.size:
                if mouse_down:
                    target.size = 0
                    score += 1
            if target.size == 0:
                targets.remove(target)

        pg.display.update()

    pg.quit()
        

main()