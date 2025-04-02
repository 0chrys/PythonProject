import pygame
import random
from config import *

class Obstacle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, GRID_CELL_SIZE, GRID_CELL_SIZE)
        self.color = (128, 128, 128)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class ObstaclesManager:
    def __init__(self):
        self.obstacles = []
        self.create_obstacles()

    def create_obstacles(self):
        # Créer des obstacles aléatoires
        for _ in range(10):  # 10 obstacles
            while True:
                x = random.randint(0, (SCREEN_SIZE // GRID_CELL_SIZE) - 1) * GRID_CELL_SIZE
                y = random.randint(0, (SCREEN_SIZE // GRID_CELL_SIZE) - 1) * GRID_CELL_SIZE
                obstacle = Obstacle(x, y)
                if not self.is_position_occupied(x, y):
                    self.obstacles.append(obstacle)
                    break

    def is_position_occupied(self, x, y):
        for obstacle in self.obstacles:
            if obstacle.rect.x == x and obstacle.rect.y == y:
                return True
        return False

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def check_collision(self, rect):
        for obstacle in self.obstacles:
            if rect.colliderect(obstacle.rect):
                return True
        return False