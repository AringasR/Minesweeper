import pygame
from ui.button import Button

class DifficultyMenu:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont(None, 48)

        self.buttons = []
        self.setup_buttons()

    def setup_buttons(self):
        presets = [
            ("Easy", lambda: self.game.set_scene("game", rows=9, cols=9, mines=10)),
            ("Medium", lambda: self.game.set_scene("game", rows=16, cols=16, mines=40)),
            ("Hard", lambda: self.game.set_scene("game", rows=30, cols=16, mines=99)),
            ("Back", lambda: self.game.set_scene("menu")),
        ]
        
        screen_w, screen_h = pygame.display.get_surface().get_size()
        button_width = 380
        button_height = 50
        spacing = 20
        total_height = len(presets) * (button_height + spacing)

        start_y = (screen_h - total_height) // 2 + 40
        center_x = (screen_w - button_width) // 2

        self.buttons = []
        for i, (label, action) in enumerate(presets):
            rect = pygame.Rect(center_x, start_y + i * (button_height + spacing), button_width, button_height)
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
        title = self.font.render("Select Difficulty", True, (50, 50, 50))
        title_rect = title.get_rect(center=(screen.get_width() // 2, 80))
        screen.blit(title, title_rect)
        for button in self.buttons:
            button.draw(screen)
