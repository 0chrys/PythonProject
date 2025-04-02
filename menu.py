import pygame
import json
from config import *

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)
        self.options = ["Jouer", "Scores", "Quitter"]
        self.selected_option = 0
        self.running = True

    def draw(self):
        self.screen.fill(BG_COLOR)
        
        # Titre
        title = self.font.render("Snake Game", True, (255, 255, 255))
        self.screen.blit(title, (SCREEN_SIZE//2 - title.get_width()//2, 100))
        
        # Options
        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i != self.selected_option else (255, 255, 0)
            text = self.small_font.render(option, True, color)
            self.screen.blit(text, (SCREEN_SIZE//2 - text.get_width()//2, 200 + i * 50))
        
        # Meilleur score
        best_score_text = self.small_font.render(f"Meilleur score: {self.get_best_score()}", True, (255, 255, 255))
        self.screen.blit(best_score_text, (10, SCREEN_SIZE - 50))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    return self.options[self.selected_option]
        return None

    def get_best_score(self):
        try:
            with open("scores.json", "r") as f:
                scores = json.load(f)
                return max(scores) if scores else 0
        except:
            return 0

    def run(self):
        while self.running:
            selected = self.handle_events()
            if selected:
                return selected
            self.draw()
            pygame.display.flip()