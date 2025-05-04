import unittest
from unittest.mock import patch, MagicMock
from scenes.game_scene import GameScene
from FileManager import FileManager

class MockGame:
    def __init__(self):
        self.running = True
        self.screen = MagicMock()
        self.set_scene = MagicMock()

class TestSaveLoadGame(unittest.TestCase):
    def setUp(self):
        self.mock_game = MockGame()

        with patch('pygame.display.set_mode') as mock_set_mode, \
             patch('pygame.font.SysFont') as mock_font, \
             patch('pygame.display.get_surface') as mock_get_surface, \
             patch('pygame.display.update') as mock_update, \
             patch('pygame.display.flip') as mock_flip:
            
            mock_set_mode.return_value = MagicMock()

            mock_font.return_value = MagicMock()
            
            mock_surface = MagicMock()
            mock_surface.get_size.return_value = (800, 600)
            mock_get_surface.return_value = mock_surface
            
            mock_update.return_value = None
            mock_flip.return_value = None
            
            self.game_scene = GameScene(self.mock_game, rows=9, cols=9, mines=10)

    def test_save_and_load_game(self):
        self.game_scene.handle_left_click(0, 0)
        
        self.game_scene.save_game()

        print("Before saving:")
        for row in self.game_scene.grid:
            for cell in row:
                print(f"Cell({cell.row}, {cell.col}) - Revealed: {cell.is_revealed}, Flagged: {cell.is_flagged}")

        self.game_scene.load_game()

        print("After loading:")
        for row in self.game_scene.grid:
            for cell in row:
                print(f"Cell({cell.row}, {cell.col}) - Revealed: {cell.is_revealed}, Flagged: {cell.is_flagged}")

        self.assertEqual(self.game_scene.mines, 10)
        self.assertEqual(self.game_scene.rows, 9)
        self.assertEqual(self.game_scene.cols, 9)
        self.assertFalse(self.game_scene.is_paused)

        self.assertTrue(self.game_scene.grid[0][0].is_revealed, "Cell (0, 0) should be revealed after loading")

if __name__ == "__main__":
    unittest.main()
