import pygame
import utils

class InputBox:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.color = utils.INACTIVE_COLOR
        self.text = ""
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active state based on click
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:  # Press Enter to finalize input
                print("Entered:", self.text)
                self.text = ""  # Clear text box after pressing Enter
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]  # Remove last character
            else:
                self.text += event.unicode  # Add typed character

    def draw(self, screen):
        # Change color based on active state
        self.color = utils.ACTIVE_COLOR if self.active else utils.INACTIVE_COLOR
        pygame.draw.rect(screen, self.color, self.rect, 2)
        txt_surface = pygame.font.Font(None, 36).render(self.text, True, utils.BLACK)
        screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))