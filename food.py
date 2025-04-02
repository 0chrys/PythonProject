import pygame
import random
from config import *

import pygame
import random
from config import *

class Food:
    def __init__(self, snake_body, obstacles):
        self.body = snake_body
        self.obstacles = obstacles
        self.rect = pygame.Rect(0, 0, FOOD_SIZE, FOOD_SIZE)
        self.reset()

    def generate_position(self):
        while True:
            x = random.randint(0, (SCREEN_SIZE // GRID_CELL_SIZE) - 1) * GRID_CELL_SIZE
            y = random.randint(0, (SCREEN_SIZE // GRID_CELL_SIZE) - 1) * GRID_CELL_SIZE
            position = pygame.Rect(x, y, FOOD_SIZE, FOOD_SIZE)
            if (position not in self.body and 
                not any(obstacle.rect.colliderect(position) for obstacle in self.obstacles.obstacles)):
                return position

    def reset(self):
        self.rect = self.generate_position()

    def draw(self, screen):
        pygame.draw.rect(screen, FOOD_COLOR, self.rect)