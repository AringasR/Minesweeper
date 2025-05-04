import pygame
import sys
import json
from ui.button import Button

class MainMenu:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont(None, 48)
        self.title_font = pygame.font.SysFont(None, 72)

        self.colors = {
            "normal": (100, 100, 100),
            "hover": (160, 160, 160),
            "click": (120, 120, 120),
            "text": (255, 255, 255),
            "border": (0, 0, 0)
        }
        
        self.buttons = []
        self.setup_buttons()

    def setup_buttons(self):
        labels = [
            ("Start", lambda: self.game.set_scene("difficulty")),
            ("Exit", self.exit_game)
        ]
        screen_w, screen_h = pygame.display.get_surface().get_size()

        button_width = 380
        button_height = 50
        spacing = 20
        total_height = len(labels) * (button_height + spacing)

        start_y = (screen_h - total_height) // 2 + 40

        min_right_margin = 30
        max_button_x = 60 

        button_x = max(screen_w - button_width - min_right_margin, max_button_x)

        self.buttons = []
        for i, (label, action) in enumerate(labels):
            rect = pygame.Rect(button_x, start_y + i * (button_height + spacing), button_width, button_height)
            self.buttons.append(Button(label, rect, action))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.VIDEORESIZE:
                pygame.display.set_mode(event.size, pygame.RESIZABLE)
                self.setup_buttons()    
            for button in self.buttons:
                button.handle_event(event)

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((200, 200, 200))

        title_surface = self.title_font.render("Minesweeper", True, (50, 50, 50))
        title_rect = title_surface.get_rect(center=(screen.get_width() // 2, 80))
        screen.blit(title_surface, title_rect)

        for button in self.buttons:
            button.draw(screen)

    def start_game(self):
        self.game.set_scene("game")

    def show_options(self):
        print("Options clicked!")

    def exit_game(self):
        self.game.running = False