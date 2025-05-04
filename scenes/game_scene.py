import pygame
import json
from FileManager import FileManager
from logic import GameLogic
from status import GameStatus
from ui.button import Button
from utils import Cell, load_gif_frames, ROWS, COLS, CELL_SIZE, BANNER_HEIGHT, FPS, WHITE, BLACK, EMOJI_FRAMES, STATUS_MESSAGES

class GameScene:
    def __init__(self, game, rows=9, cols=9, mines=10, grid_data=None, game_over=False):
        
        self.FileManager = FileManager()
        
        self.game = game
        self.rows, self.cols, self.mines = rows, cols, mines

        self.is_paused = False

        self.resume_button = Button("Resume", pygame.Rect(250, 200, 300, 60), self.resume_game)
        self.save_button = Button("Save", pygame.Rect(250, 300, 300, 60), self.save_game)
        self.load_button = Button("Load", pygame.Rect(250, 400, 300, 60), self.load_game)
        self.exit_button = Button("Exit to Main Menu", pygame.Rect(250, 500, 300, 60), self.exit_to_main_menu)

        min_window_width = 400
        min_window_height = 400 
        self.window_width, self.window_height = pygame.display.get_surface().get_size()

        self.window_width = max(self.window_width, min_window_width)
        self.window_height = max(self.window_height, min_window_height)

        self.update_grid_size()

        if grid_data:
            self.grid = [[Cell(cell_data['row'], cell_data['col'], self.cell_size) for cell_data in row] for row in grid_data]
        else:
            self.grid = [[Cell(row, col, self.cell_size) for col in range(self.cols)] for row in range(self.rows)]

        self.game.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)

        self.game_logic = GameLogic(self.rows, self.cols, self.mines)

        self.status = GameStatus(EMOJI_FRAMES, STATUS_MESSAGES)
        self.emoji_frame_timer = 0
        self.game_over = False

    def resume_game(self):
        """Function to resume the game"""
        self.is_paused = False

    def update_grid_size(self):
        max_cell_w = self.window_width // self.cols
        max_cell_h = (self.window_height - BANNER_HEIGHT) // self.rows
        self.cell_size = min(max_cell_w, max_cell_h)

        self.saved_cell_states = {}
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.grid[row][col] if hasattr(self, 'grid') else None  
                if cell:
                    self.saved_cell_states[(row, col)] = {
                        "is_flagged": cell.is_flagged,
                        "is_questioned": cell.is_questioned
                    }

        grid_width = self.cols * self.cell_size
        grid_height = self.rows * self.cell_size
        total_height = grid_height + BANNER_HEIGHT

        self.window_width = max(grid_width, 400)
        self.window_height = max(total_height, 400)

        self.game.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)

        self.left_margin = (self.window_width - grid_width) // 2
        self.top_margin = (self.window_height - total_height) // 2

        self.grid = [[Cell(row, col, self.cell_size) for col in range(self.cols)] for row in range(self.rows)]

        for row in range(self.rows):
            for col in range(self.cols):
                if (row, col) in self.saved_cell_states:
                    state = self.saved_cell_states[(row, col)]
                    cell = self.grid[row][col]
                    cell.is_flagged = state["is_flagged"]
                    cell.is_questioned = state["is_questioned"]
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_paused = not self.is_paused

            elif event.type == pygame.VIDEORESIZE:
                self.window_width, self.window_height = event.size
                self.window_width = max(self.window_width, 400)
                self.window_height = max(self.window_height, 400)
                self.update_grid_size()

                self.game.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)

                self.grid = [[Cell(row, col, self.cell_size) for col in range(self.cols)] for row in range(self.rows)]
                self.sync_all_cells()

            if self.is_paused:
                self.resume_button.handle_event(event)
                self.save_button.handle_event(event)
                self.load_button.handle_event(event)
                self.exit_button.handle_event(event)

            elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                x, y = pygame.mouse.get_pos()
                if y < BANNER_HEIGHT:
                    return
                col = (x - self.left_margin) // self.cell_size
                row = (y - BANNER_HEIGHT) // self.cell_size
                if not (0 <= row < self.rows and 0 <= col < self.cols):
                    return

                if pygame.mouse.get_pressed(3) == (1, 0, 1):
                    self.handle_chord_click(row, col)
                    return

                if event.button == 1:
                    self.handle_left_click(row, col)
                elif event.button == 3:
                    self.handle_right_click(row, col)

    def update(self):
        self.emoji_frame_timer += 1
        if self.emoji_frame_timer >= 4:
            self.status.update_frame()
            self.emoji_frame_timer = 0

    def draw(self, screen):
        screen.fill((160, 160, 160))
        self.draw_banner(screen)
        for row in self.grid:
            for cell in row:
                x_pos = self.left_margin + cell.col * self.cell_size
                y_pos = self.top_margin + BANNER_HEIGHT + cell.row * self.cell_size

                cell.rect = pygame.Rect(x_pos, y_pos, self.cell_size, self.cell_size)
        
                cell.draw(screen, cell.rect)

        if self.is_paused:
            pause_background = pygame.Rect(0, 0, self.window_width, self.window_height)
            pygame.draw.rect(screen, (0, 0, 0), pause_background)

            button_width = 300
            button_height = 60
            button_spacing = 20

            total_buttons_height = (button_height * 4) + (button_spacing * 3)

            start_y = (self.window_height - total_buttons_height) // 2

            self.resume_button.rect.topleft = (self.window_width // 2 - button_width // 2, start_y)
            self.save_button.rect.topleft = (self.window_width // 2 - button_width // 2, start_y + button_height + button_spacing)
            self.load_button.rect.topleft = (self.window_width // 2 - button_width // 2, start_y + 2 * (button_height + button_spacing))
            self.exit_button.rect.topleft = (self.window_width // 2 - button_width // 2, start_y + 3 * (button_height + button_spacing))

            self.resume_button.draw(screen, center_text=True)
            self.save_button.draw(screen, center_text=True)
            self.load_button.draw(screen, center_text=True)
            self.exit_button.draw(screen, center_text=True)

    def draw_banner(self, screen):
        banner_rect = pygame.Rect(0, 0, self.game.screen.get_width(), BANNER_HEIGHT)
        pygame.draw.rect(screen, (220, 220, 220), banner_rect)
        pygame.draw.line(screen, BLACK, (0, BANNER_HEIGHT), (self.game.screen.get_width(), BANNER_HEIGHT), 2)

        emoji_frame = self.status.get_frame()
        screen.blit(emoji_frame, (10, 6))

        text_surface = self.game.emoji_text_font.render(self.status.get_text(), True, (30, 30, 30))
        text_rect = text_surface.get_rect(midleft=(60, BANNER_HEIGHT // 2))
        screen.blit(text_surface, text_rect)

    def handle_left_click(self, row, col):
        cell = self.grid[row][col]
        if cell.is_flagged or cell.is_questioned:
            return
        result = self.game_logic.reveal_cell(row, col)
        self.sync_all_cells()
        if result == "mine":
            cell.was_triggered = True
            self.status.set("shocked")
            self.game_over = True
            self.reveal_all_cells()
        elif result == "safe":
            self.status.set("happy")
            if self.game_logic.check_win():
                self.status.set("win")
                self.game_over = True
                self.reveal_all_cells()

    def handle_right_click(self, row, col):
        cell = self.grid[row][col]
        if cell.is_revealed:
            return

        if cell.is_flagged:
            cell.is_flagged = False
            cell.is_questioned = True
        elif cell.is_questioned:
            cell.is_questioned = False
        else:
            cell.is_flagged = True

        self.game_logic.grid.grid[row][col]['is_flagged'] = cell.is_flagged

    def handle_chord_click(self, row, col):
        flagged_count = 0
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if self.grid[nr][nc].is_flagged:
                        flagged_count += 1

        logic_cell = self.game_logic.grid.grid[row][col]
        if not logic_cell['is_revealed']:
            return

        if flagged_count == logic_cell['neighbor_mines']:
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    nr, nc = row + dr, col + dc
                    if dr == 0 and dc == 0:
                        continue
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        neighbor = self.grid[nr][nc]
                        if not neighbor.is_revealed and not neighbor.is_flagged:
                            result = self.game_logic.reveal_cell(nr, nc)
                            if result == "mine":
                                neighbor.was_triggered = True
                                self.status.set("shocked")
                                self.game_over = True
                                self.reveal_all_cells()
                                return

            self.sync_all_cells()

            if self.game_logic.check_win():
                self.status.set("win")
                self.game_over = True
                self.reveal_all_cells()
            else:
                self.status.set("happy")

    def sync_all_cells(self):
        for row_index in range(self.rows):
            for col_index in range(self.cols):
                logic_cell = self.game_logic.grid.grid[row_index][col_index]
                ui_cell = self.grid[row_index][col_index]
                if logic_cell['is_revealed']:
                    ui_cell.reveal()
                    ui_cell.neighbor_mines = logic_cell['neighbor_mines']

                ui_cell.logic_cell_ref = logic_cell
                ui_cell.game_over = self.game_over
                ui_cell.is_flagged = logic_cell.get('is_flagged', ui_cell.is_flagged)
                ui_cell.is_questioned = logic_cell.get('is_questioned', ui_cell.is_questioned)

                if ui_cell.is_flagged or ui_cell.is_questioned:
                    ui_cell.was_triggered = False

    def reveal_all_cells(self):
        self.sync_all_cells()
        for row_index in range(self.rows):
            for col_index in range(self.cols):
                cell = self.grid[row_index][col_index]
                cell.logic_cell_ref = self.game_logic.grid.grid[row_index][col_index]
                cell.game_over = True

    def save_game(self):
        """Function to save the game state"""
        try:
            self.FileManager.save_game(self.grid, self.rows, self.cols, self.mines, self.game_over, self.is_paused)
            self.is_paused = False
            print("Game saved successfully, unpaused.")
        except Exception as e:
            print(f"Error while saving the game: {e}")

    def load_game(self):
        """Function to load the game state"""
        print("Loading the game...")
        game_data = self.FileManager.load_game()

        if game_data:
            self.rows = game_data['rows']
            self.cols = game_data['cols']
            self.mines = game_data['mines']
            self.game_over = game_data['game_over']
            self.is_paused = game_data['is_paused']
            self.grid = [[Cell(cell_data['row'], cell_data['col'], self.cell_size) for cell_data in row]
                        for row in game_data['grid']]

            for row_index, row in enumerate(self.grid):
                for col_index, cell in enumerate(row):
                    cell_data = game_data['grid'][row_index][col_index]
                    cell.is_revealed = cell_data['is_revealed']
                    cell.is_flagged = cell_data['is_flagged']
                    cell.is_questioned = cell_data['is_questioned']
                    cell.neighbor_mines = cell_data['neighbor_mines']

            print("Game loaded!")
            self.is_paused = False
        else:
            print("No saved game found!")

    def exit_to_main_menu(self):
        self.game.set_scene("menu")
        print("Exiting to main menu...")