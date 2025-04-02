import pygame
from pygame import Vector2
from random import randrange
from config import *

class Snake:
    def __init__(self):
        self.body = [pygame.Rect(SCREEN_SIZE//2, SCREEN_SIZE//2, GRID_CELL_SIZE, GRID_CELL_SIZE)]
        self.direction = Vector2(0, -SNAKE_MOVE_LENGHT)
        self.new_block = False
        self.color = (0, 255, 0)

    def move(self):
        if self.direction != Vector2(0, 0):
            new_head = self.body[0].copy()
            new_head.move_ip(self.direction)
            self.body.insert(0, new_head)
            if not self.new_block:
                self.body.pop()
            self.new_block = False

    def grow(self):
        self.new_block = True

    def draw(self, screen):
        for block in self.body:
            pygame.draw.rect(screen, self.color, block)

    def check_collision(self, obstacles=None):
        # Vérification des collisions avec les murs
        if not 0 <= self.body[0].x < SCREEN_SIZE or not 0 <= self.body[0].y < SCREEN_SIZE:
            return True
        # Vérification des collisions avec le corps
        for block in self.body[1:]:
            if self.body[0].colliderect(block):
                return True
        # Vérification des collisions avec les obstacles
        if obstacles and obstacles.check_collision(self.body[0]):
            return True
        return False