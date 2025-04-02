import pygame
from random import randint

class Effects:
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.particles = []
        self.explosion_sounds = []
        self.load_sounds()

    def load_sounds(self):
        # Charger les effets sonores
        pass  # À implémenter avec des fichiers son

    def add_particle(self, pos, color, size=3):
        self.particles.append({
            'pos': pygame.Vector2(pos),
            'vel': pygame.Vector2(randint(-3, 3), randint(-3, 3)),
            'size': size,
            'color': color,
            'lifetime': 20
        })

    def update_particles(self):
        for particle in self.particles[:]:
            particle['pos'] += particle['vel']
            particle['vel'].y += 0.05  # Gravité légère
            particle['lifetime'] -= 1
            if particle['lifetime'] <= 0:
                self.particles.remove(particle)

    def draw_particles(self, screen):
        for particle in self.particles:
            # Effet de flou léger
            for i in range(3):
                pygame.draw.circle(screen, (*particle['color'], 100), 
                                 (int(particle['pos'].x), int(particle['pos'].y)),
                                 particle['size'] + i, 1)
            pygame.draw.circle(screen, particle['color'], 
                             (int(particle['pos'].x), int(particle['pos'].y)),
                             particle['size'])

    def create_explosion(self, pos, color=(255, 255, 0), count=15):
        for _ in range(count):
            self.add_particle(pos, color)