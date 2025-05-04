import pygame

class ButtonBase:
    def __init__(self, text, rect, action):
        self.text = text
        self.rect = rect
        self.action = action
        self.pressed = False

    def draw(self, screen):
        pass  # To be overridden by subclasses

    def handle_event(self, event):
        pass  # To be overridden by subclasses

class Button(ButtonBase):
    def __init__(self, text, rect, action):
        super().__init__(text, rect, action)
        self.colors = {
            "normal": (100, 100, 100),
            "hover": (160, 160, 160),
            "click": (120, 120, 120),
            "text": (255, 255, 255),
            "border": (0, 0, 0),
        }

        self.font = pygame.font.SysFont(None, 48)
        self.text_surface = self.font.render(self.text, True, self.colors["text"])
        self.text_rect = self.text_surface.get_rect(midleft=(self.rect.left + 10, self.rect.centery))

    def draw(self, screen, center_text=False):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)

        if self.pressed:
            color = self.colors["click"]
        elif is_hovered:
            color = self.colors["hover"]
        else:
            color = self.colors["normal"]

        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, self.colors["border"], self.rect, 2)

        if center_text:
            self.text_rect.center = self.rect.center
        else:
            self.text_rect.midleft = (self.rect.left + 10, self.rect.centery)

        screen.blit(self.text_surface, self.text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.pressed = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.pressed and self.rect.collidepoint(pygame.mouse.get_pos()):
                self.action()
            self.pressed = False
