import pygame
from PIL import Image

# Constants
ROWS, COLS = 10, 10
CELL_SIZE = 40
BANNER_HEIGHT = 60
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE + BANNER_HEIGHT
FPS = 60

GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def load_gif_frames(filename):
    pil_gif = Image.open(filename)
    frames = []
    try:
        while True:
            frame = pil_gif.convert("RGBA")
            pygame_image = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
            pygame_image = pygame.transform.scale(pygame_image, (48, 48))
            frames.append(pygame_image)
            pil_gif.seek(pil_gif.tell() + 1)
    except EOFError:
        pass
    return frames

EMOJI_FRAMES = {
            "neutral": load_gif_frames("assets/emoji/neutral.gif"),
            "happy": load_gif_frames("assets/emoji/happy.gif"),
            "win": load_gif_frames("assets/emoji/win.gif"),
            "shocked": load_gif_frames("assets/emoji/shocked.gif"),
        }

STATUS_MESSAGES = {
            "neutral": ["Welcome to Minesweeper!"],
            "happy": ["Nice! No mine here!", "Safe! Keep going!", "Clean move!"],
            "shocked": ["Boom! You hit a mine!", "Oh no! You stepped on a mine!", "💥 Mine detonated! Oops!"],
            "win": ["Congratulations! You've cleared the minefield!", "You win! 🎉", "Victory! Minefield cleared!"]
        }

class Cell:
    @staticmethod
    def load_and_scale_image(path, size):
        image = pygame.image.load(path)
        return pygame.transform.scale(image, size)

    def __init__ (self, row, col, size):
        self.row = row
        self.col = col
        self.size = size
        self.rect = pygame.Rect(
            col * size,
            row * size + BANNER_HEIGHT,
            size,
            size
        )
        self.is_revealed = False
        self.neighbor_mines = 0
        self.is_flagged = False
        self.is_questioned = False
        self.was_triggered = False

        self.flag_image = self.load_and_scale_image("assets/icons/flag.png", (CELL_SIZE - 10, CELL_SIZE - 10))
        self.question_image = self.load_and_scale_image("assets/icons/question.png", (CELL_SIZE - 10, CELL_SIZE - 10))
        self.mine_image = self.load_and_scale_image("assets/icons/mine.png", (24, 24))
        self.mine_exploded_image = self.load_and_scale_image("assets/icons/mine_exploded.png", (24, 24))
        self.correct_flag_image = self.load_and_scale_image("assets/icons/correct_flag.png", (16, 16))
        self.wrong_flag_image = self.load_and_scale_image("assets/icons/wrong_flag.png", (16, 16))

    def to_dict(self):
        return {
            'row': self.row,
            'col': self.col,
            'is_revealed': self.is_revealed,
            'is_flagged': self.is_flagged,
            'is_questioned': self.is_questioned,
            'neighbor_mines': self.neighbor_mines,
        }

    def draw(self, screen, rect=None):
        cell_rect = rect if rect else self.rect
        color = GRAY if self.is_revealed else DARK_GRAY
        pygame.draw.rect(screen, color, cell_rect)
        pygame.draw.rect(screen, BLACK, cell_rect, 1)

        if self.was_triggered:
                exploded_rect = self.mine_exploded_image.get_rect(center=cell_rect.center)
                screen.blit(self.mine_exploded_image, exploded_rect)
                return

        if not self.is_revealed:
            if self.is_flagged:
                flag_rect = self.flag_image.get_rect(center=self.rect.center)
                screen.blit(self.flag_image, flag_rect)
            elif self.is_questioned:
                question_rect = self.question_image.get_rect(center=self.rect.center)
                screen.blit(self.question_image, question_rect)
            
            if hasattr(self, 'game_over') and self.game_over:
                logic_cell = self.logic_cell_ref

                if self.was_triggered:
                    exploded_rect = self.mine_exploded_image.get_rect(center=cell_rect.center)
                    screen.blit(self.mine_exploded_image, exploded_rect)

                if logic_cell['is_mine'] and not self.is_flagged:
                    mine_rect = self.mine_image.get_rect(center=cell_rect.center)
                    screen.blit(self.mine_image, mine_rect)

                elif self.is_flagged:
                    if logic_cell['is_mine']:
                        tick_rect = (self.correct_flag_image.get_rect(bottomright=cell_rect.bottomright))
                        screen.blit(self.correct_flag_image, tick_rect)
                    else:
                        cross_rect = self.wrong_flag_image.get_rect(bottomright=cell_rect.bottomright)
                        screen.blit(self.wrong_flag_image, cross_rect)

        if self.is_revealed and self.neighbor_mines > 0:
            number_colors = {
                1: (0, 0, 255),
                2: (0, 128, 0),
                3: (255, 0, 0),
                4: (128, 0, 128),
                5: (128, 0, 0),   
                6: (0, 128, 128),
                7: (0, 0, 0), 
                8: (128, 128, 128) 
            }
            text_color = number_colors.get(self.neighbor_mines, BLACK)

            font = pygame.font.SysFont(None, 24)
            text = font.render(str(self.neighbor_mines), True, text_color)
            text_rect = text.get_rect(center=cell_rect.center)
            screen.blit(text, text_rect)

    def sync_with_logic(self, logic):
        logic_data = logic.grid[self.row][self.col]
        self.is_revealed = logic_data.get('is_revealed', self.is_revealed)
        self.neighbor_mines = logic_data.get('neighbor_mines', self.neighbor_mines)
        self.is_flagged = logic_data.get('is_flagged', self.is_flagged)

    def reveal(self):
        self.is_revealed = True
    