import pygame
import utils

class Plant:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.circle(screen, utils.GREEN, (self.x, self.y), 3)