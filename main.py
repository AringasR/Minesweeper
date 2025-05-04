import pygame
from scenes.main_menu import MainMenu
from scenes.game_scene import GameScene
from utils import WIDTH, HEIGHT, FPS

class Game:
    def __init__(self):
        pygame.init()
        self.emoji_text_font = pygame.font.Font("assets/fonts/seguiemj.ttf", 24)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Minesweeper")
        self.clock = pygame.time.Clock()
        self.running = True
        self.scene = None

    def set_scene(self, name, **kwargs):
        if name == "menu":
            from scenes.main_menu import MainMenu
            self.scene = MainMenu(self)
        elif name == "game":
            self.show_loading("Generating Game...")
            pygame.display.flip()
            from scenes.game_scene import GameScene
            self.scene = GameScene(self, **kwargs)    
        elif name == "difficulty":
            from scenes.difficulty_menu import DifficultyMenu
            self.scene = DifficultyMenu(self)

    def run(self):
        self.set_scene("menu")

        while self.running:
            events = pygame.event.get()
            self.scene.handle_events(events)
            self.scene.update()
            self.scene.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()

    def show_loading(self, message="Loading..."):
        self.screen.fill((30, 30, 30))
        font = pygame.font.SysFont(None, 48)
        text = font.render(message, True, (255, 255, 255))
        rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text, rect)
        pygame.display.flip()

def show_loading_screen(screen):
    screen.fill((30, 30, 30))
    font = pygame.font.SysFont(None, 48)
    text = font.render("Loading...", True, (255, 255, 255))
    rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(text, rect)
    pygame.display.flip()
    pygame.time.delay(1000)

if __name__ == "__main__":
    game = Game()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Minesweeper")

    show_loading_screen(screen)

    game = Game()
    game.screen = screen
    game.run()