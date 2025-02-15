import pygame
import random
import utils

class Predator:
    def __init__(self, x, y, speed=None, hunting_efficiency=None):
        self.x = x
        self.y = y
        self.energy = 150
        self.speed = speed if speed is not None else random.randint(1, 5)
        self.hunting_efficiency = hunting_efficiency if hunting_efficiency is not None else random.uniform(0.5, 1.5)

    def move(self):
        self.x += random.choice([-self.speed, 0, self.speed])
        self.y += random.choice([-self.speed, 0, self.speed])
        self.energy -= 2 / self.hunting_efficiency  # Decrease energy based on hunting efficiency

    def hunt(self, herbivores):
        for herbivore in herbivores:
            if abs(self.x - herbivore.x) < 8 and abs(self.y - herbivore.y) < 8:
                herbivores.remove(herbivore)
                self.energy += 50 * self.hunting_efficiency  # Gain more energy based on hunting efficiency

    def breed(self, partner):
        # Simple breeding mechanism: average the traits
        child_speed = (self.speed + partner.speed) // 2
        child_hunting_efficiency = (self.hunting_efficiency + partner.hunting_efficiency) / 2
        child_x = random.randint(0, 800)  # Random x position
        child_y = random.randint(0, 600)  # Random y position
        return Predator(child_x, child_y, child_speed, child_hunting_efficiency)

    def draw(self, screen):
        pygame.draw.circle(screen, utils.RED, (self.x, self.y), 8)
