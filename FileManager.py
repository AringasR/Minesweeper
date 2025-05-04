import json

class FileManager:
    def __init__(self, file_name="game_save.json"):
        self.file_name = file_name

    def save_game(self, grid, rows, cols, mines, game_over, is_paused):
        game_data = {
            'grid': [[cell.to_dict() for cell in row] for row in grid],
            'mines': mines,
            'rows': rows,
            'cols': cols,
            'game_over': game_over,
            'is_paused': is_paused,
        }
        
        try:
            with open(self.file_name, "w") as f:
                json.dump(game_data, f)
            print("Game saved!")
        except Exception as e:
            print(f"Error saving game: {e}")

    def load_game(self):
        try:
            with open(self.file_name, "r") as f:
                game_data = json.load(f)
            
            return game_data
        except FileNotFoundError:
            print("No saved game found!")
            return None
        except Exception as e:
            print(f"Error loading game: {e}")
            return None