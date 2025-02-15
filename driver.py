import pygame, random
import sys
from Plant import Plant
from Predator import Predator
from Herbivore import Herbivore
from Button import Button
import matplotlib.pyplot as plt

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ecosystem Simulator")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
BLUE = (70, 130, 180)

# Fonts
font = pygame.font.Font(None, 36)

plants, predators, herbivores = None, None, None

def draw_text(text, x, y, color=BLACK):
    render = font.render(text, True, color)
    screen.blit(render, (x, y))

def home_screen():
    input_active = False
    user_text = ["", ""]
    input_boxes = [
        pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 40, 200, 40),
        pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 40)
    ]
    start_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 200, 150, 50)
    
    while True:
        screen.fill(WHITE)
        draw_text("Ecosystem Simulator", WIDTH // 2 - 140, HEIGHT // 4)
        draw_text("Prey:", WIDTH // 2 - 140, HEIGHT // 2 + 20)
        draw_text("Predators:", WIDTH // 2 - 140, HEIGHT // 2 + 80)
        
        for box in input_boxes:
            pygame.draw.rect(screen, BLACK, box, 2)
        pygame.draw.rect(screen, GREEN, start_button)
        draw_text("Start", WIDTH // 2 - 60, HEIGHT // 2 + 210, WHITE)
        
        for i in range(2):
            txt_surface = font.render(user_text[i], True, BLACK)
            screen.blit(txt_surface, (input_boxes[i].x + 10, input_boxes[i].y + 10))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, box in enumerate(input_boxes):
                    if box.collidepoint(event.pos):
                        input_active = [False, False, False]
                        input_active[i] = True
                if start_button.collidepoint(event.pos):
                    simulation_screen(user_text)
            elif event.type == pygame.KEYDOWN:
                for i in range(3):
                    if input_active[i]:
                        if event.key == pygame.K_RETURN:
                            input_active[i] = False
                        elif event.key == pygame.K_BACKSPACE:
                            user_text[i] = user_text[i][:-1]
                        elif event.unicode.isdigit():
                            user_text[i] += event.unicode
        
        pygame.display.flip()

def plot_graph(days, plant_pop, herbivore_pop, predator_pop):
    plt.figure(figsize=(6, 4))
    plt.plot(days, plant_pop, label='Plants', color='green')
    plt.plot(days, herbivore_pop, label='Herbivores', color='blue')
    plt.plot(days, predator_pop, label='Predators', color='red')
    plt.xlabel('Days')
    plt.ylabel('Population')
    plt.title('Ecosystem Population Over Time')
    plt.legend()
    plt.show()


def simulation_screen(user_text):
    days = []
    plant_pop = []
    herbivore_pop = []
    predator_pop = []
    day_count = 0

    plants = [Plant(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(50)]
    herbivores = [Herbivore(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(int(user_text[0]))]
    predators = [Predator(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(int(user_text[1]))]
    
    running = True
    paused = False

    # Create buttons
    pause_button = Button(10, 10, 120, 40, "Pause/Unpause", lambda: toggle_pause())
    skip_button = Button(10, 60, 120, 40, "Skip to End", lambda: skip_to_end())

    def toggle_pause():
        nonlocal paused
        paused = not paused

    def skip_to_end():
        nonlocal day_count, running

        while herbivores and predators and running:
            update_simulation(plants, herbivores, predators)  # Single fast run
            days.append(day_count)
            plant_pop.append(len(plants))
            herbivore_pop.append(len(herbivores))
            predator_pop.append(len(predators))
            day_count += 1

        # Process the final state only once
        screen.fill(BLUE)
        draw_simulation(plants, herbivores, predators)
        pygame.display.flip()


    while running:
        screen.fill(BLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if pause_button.is_clicked(event.pos):
                        pause_button.action()
                    elif skip_button.is_clicked(event.pos):
                        skip_button.action()

        if len(predators) == 0 and len(herbivores) == 0:
            break
        elif not paused:
            update_simulation(plants, herbivores, predators)

        draw_simulation(plants, herbivores, predators)

        # Draw buttons
        pause_button.draw(screen)
        skip_button.draw(screen)

        days.append(day_count)
        plant_pop.append(len(plants))
        herbivore_pop.append(len(herbivores))
        predator_pop.append(len(predators))
        day_count += 1

        pygame.display.flip()
        pygame.time.Clock().tick(30)  # Control frame rate based on speed

    pygame.quit()
    plot_graph(days, plant_pop, herbivore_pop, predator_pop)
    plt.close()
    sys.exit()

def update_simulation(plants, herbivores, predators):
    # Update herbivores
    for herbivore in herbivores[:]:
        herbivore.move()
        herbivore.eat(plants)
        if herbivore.energy <= 0:
            herbivores.remove(herbivore)

    # Update predators
    for predator in predators[:]:
        predator.move()
        predator.hunt(herbivores)
        if predator.energy <= 0:
            predators.remove(predator)

    # Breeding logic for herbivores
    for i in range(len(herbivores)):
        for j in range(i + 1, len(herbivores)):
            if (herbivores[i].energy > 50 and herbivores[j].energy > 50 and
                abs(herbivores[i].x - herbivores[j].x) < 10 and
                abs(herbivores[i].y - herbivores[j].y) < 10):
                offspring = herbivores[i].breed(herbivores[j])
                herbivores.append(offspring)
                herbivores[i].energy -= 20  # Energy cost of breeding
                herbivores[j].energy -= 20
                break  # Break to avoid breeding multiple times in one frame

    # Breeding logic for predators
    for i in range(len(predators)):
        for j in range(i + 1, len(predators)):
            if (predators[i].energy > 60 and predators[j].energy > 60 and
                abs(predators[i].x - predators[j].x) < 10 and
                abs(predators[i].y - predators[j].y) < 10):
                offspring = predators[i].breed(predators[j])
                predators.append(offspring)
                predators[i].energy -= 30  # Energy cost of breeding
                predators[j].energy -= 30
                break  # Break to avoid breeding multiple times in one frame

def draw_simulation(plants, herbivores, predators):
    # Draw plants
    for plant in plants:
        plant.draw(screen)
    
    # Draw herbivores
    for herbivore in herbivores:
        herbivore.draw(screen)

    # Draw predators
    for predator in predators:
        predator.draw(screen)

# Run the home screen first
home_screen()




