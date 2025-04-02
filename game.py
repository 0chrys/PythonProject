import pygame
import pygame
from pygame import Vector2
from snake import Snake
from food import Food
from config import *
from scores import Scores
from effects import Effects
from menu import Menu  
from sounds import Sounds  
from obstacles import ObstaclesManager

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.running = True
        self.begin = True
        self.game_over = False
        self.score = 0
        self.best_score = 0
        self.snake = None
        self.food = None
        self.obstacles = None
        self.time = 0
        self.scores = Scores()
        self.best_score = self.scores.get_best_score()
        self.effects = Effects(SCREEN_SIZE)
        self.menu = Menu(self.screen)
        self.death_effect_time = None
        self.death_effect_duration = 1000
        self.sounds = Sounds()

    def reset(self):
        self.begin = False
        self.game_over = False
        self.score = 0
        self.snake = Snake()
        self.obstacles = ObstaclesManager()  # Créer les obstacles d'abord
        self.food = Food(self.snake.body, self.obstacles)  # Passe les obstacles
        self.time = pygame.time.get_ticks()

    def update(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.time > DELAY:
            self.time = time_now
            self.snake.move()
            if self.snake.body[0].colliderect(self.food.rect):
                self.snake.grow()
                self.food.reset()
                self.score += 10
                if self.score > self.best_score:
                    self.best_score = self.score
                    self.scores.add_score(self.score)
                self.effects.create_explosion(self.food.rect.center, (255, 255, 255), count=10)
                self.sounds.play('eat')
            if self.snake.check_collision(self.obstacles):
                self.game_over = True
                self.death_effect_time = time_now
                self.effects.create_explosion(self.snake.body[0].center, (255, 0, 0), count=20)
                self.sounds.play('death')

    def draw(self):
        self.screen.fill(BG_COLOR)
        # Dessin de la grille
        for i in range(0, SCREEN_SIZE, GRID_CELL_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, start_pos=(i, 0), end_pos=(i, SCREEN_SIZE))
            pygame.draw.line(self.screen, GRID_COLOR, start_pos=(0, i), end_pos=(SCREEN_SIZE, i))
        self.food.draw(self.screen)
        self.snake.draw(self.screen)
        self.obstacles.draw(self.screen)
        # Affichage des scores
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        best_score_text = self.font.render(f"Meilleur: {self.best_score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(best_score_text, (10, 50))
        # Dessin des effets
        self.effects.draw_particles(self.screen)
        self.effects.update_particles()
        # Affichage de l'effet de mort
        if self.game_over and self.death_effect_time:
            time_now = pygame.time.get_ticks()
            progress = min((time_now - self.death_effect_time) / self.death_effect_duration, 1)
            alpha = int(255 * (1 - progress))
            overlay = pygame.Surface((SCREEN_SIZE, SCREEN_SIZE))
            overlay.fill((255, 0, 0, alpha))
            self.screen.blit(overlay, (0, 0))
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.begin = True
                        self.game_over = False
                    elif self.begin:
                        self.begin = False
                elif not self.game_over:
                    self.handle_key(event.key)

    def handle_key(self, key):
        if key == pygame.K_UP and self.snake.direction != Vector2(0, SNAKE_MOVE_LENGHT):
            self.snake.direction = Vector2(0, -SNAKE_MOVE_LENGHT)
        if key == pygame.K_DOWN and self.snake.direction != Vector2(0, -SNAKE_MOVE_LENGHT):
            self.snake.direction = Vector2(0, SNAKE_MOVE_LENGHT)
        if key == pygame.K_RIGHT and self.snake.direction != Vector2(-SNAKE_MOVE_LENGHT, 0):
            self.snake.direction = Vector2(SNAKE_MOVE_LENGHT, 0)
        if key == pygame.K_LEFT and self.snake.direction != Vector2(SNAKE_MOVE_LENGHT, 0):
            self.snake.direction = Vector2(-SNAKE_MOVE_LENGHT, 0)

    def run(self):
        while self.running:
            menu_choice = self.menu.run()
            if menu_choice == "Jouer":
                self.game_loop()
            elif menu_choice == "Scores":
                self.show_scores()
            elif menu_choice == "Quitter":
                self.running = False

    def quit(self):
        pygame.quit()

    def show_game_over(self):
        self.screen.fill(BG_COLOR)
        game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        best_score_text = self.font.render(f"Meilleur: {self.best_score}", True, (255, 255, 255))
        restart_text = self.font.render("Appuyez sur ESPACE pour rejouer", True, (255, 255, 255))
        
        self.screen.blit(game_over_text, (SCREEN_SIZE//2 - game_over_text.get_width()//2, SCREEN_SIZE//3))
        self.screen.blit(score_text, (SCREEN_SIZE//2 - score_text.get_width()//2, SCREEN_SIZE//2))
        self.screen.blit(best_score_text, (SCREEN_SIZE//2 - best_score_text.get_width()//2, SCREEN_SIZE//2 + 40))
        self.screen.blit(restart_text, (SCREEN_SIZE//2 - restart_text.get_width()//2, SCREEN_SIZE//2 + 80))
    def game_loop(self):
        while self.running:
            self.handle_events()
            if self.begin:
                self.reset()
            elif not self.game_over:
                self.update()
                self.draw()
            else:
                time_now = pygame.time.get_ticks()
                if self.death_effect_time and time_now - self.death_effect_time > self.death_effect_duration:
                    self.show_game_over()
                else:
                    self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)

    def show_scores(self):
        self.screen.fill(BG_COLOR)
        title = self.font.render("Meilleurs Scores", True, (255, 255, 255))
        self.screen.blit(title, (SCREEN_SIZE//2 - title.get_width()//2, 100))
        
        scores = self.scores.get_scores()
        for i, score in enumerate(scores):
            text = self.font.render(f"{i+1}. {score}", True, (255, 255, 255))
            self.screen.blit(text, (SCREEN_SIZE//2 - text.get_width()//2, 200 + i * 50))
        
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                        event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                ):
                    waiting = False        