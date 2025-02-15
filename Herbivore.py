import pygame, random
import utils

class Herbivore:
    def __init__(self, x, y, speed=None, energy_efficiency=None):
        self.x = x
        self.y = y
        self.energy = 100
        self.speed = speed if speed is not None else random.randint(1, 5)
        self.energy_efficiency = energy_efficiency if energy_efficiency is not None else random.uniform(0.5, 1.5)

    def move(self):
        self.x += random.choice([-self.speed, 0, self.speed])
        self.y += random.choice([-self.speed, 0, self.speed])
        self.energy -= 1 / self.energy_efficiency  # Decrease energy based on efficiency

    def eat(self, plants):
        for plant in plants:
            if abs(self.x - plant.x) < 5 and abs(self.y - plant.y) < 5:
                plants.remove(plant)
                self.energy += 30 * self.energy_efficiency  # Gain more energy based on efficiency
    
    def breed(self, partner):
        # Simple breeding mechanism: average the traits
        child_speed = (self.speed + partner.speed) // 2
        child_energy_efficiency = (self.energy_efficiency + partner.energy_efficiency) / 2
        child_x = random.randint(0, 800)  # Random x position
        child_y = random.randint(0, 600)  # Random y position
        return Herbivore(child_x, child_y, child_speed, child_energy_efficiency)

    def draw(self, screen):
        pygame.draw.circle(screen, utils.BLUE, (self.x, self.y), 6)