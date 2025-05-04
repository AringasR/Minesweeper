import random

class GameComponent:
    def __init__(self):
        pass

    def check_win(self):
        return none

class Grid(GameComponent):
    def __init__(self, rows, cols, mine_count):
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.mine_count = mine_count
        self.grid = [[{
            'is_mine': False,
            'is_revealed': False,
            'is_flagged': False,
            'neighbor_mines': 0
        } for _ in range(cols)] for _ in range(rows)]

    def place_mines(self, safe_row, safe_col):
        positions = set()
        excluded = set()

        print(f"Placing mines around safe cell: ({safe_row}, {safe_col})")

        for delta_row in (-1, 0, 1):
            for delta_col in (-1, 0, 1):
                row, col = safe_row + delta_row, safe_col + delta_col
                if 0 <= row < self.rows and 0 <= col < self.cols:
                    excluded.add((row, col))

        print(f"Excluded cells: {excluded}")

        while len(positions) < self.mine_count:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if (row, col) not in excluded and not self.grid[row][col]['is_mine']:
                positions.add((row, col))

        print(f"Mine positions: {positions}")

        for row, col in positions:
            self.grid[row][col]['is_mine'] = True

        self._calculate_neighbors()

    def _calculate_neighbors(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col]['is_mine']:
                    continue
                self.grid[row][col]['neighbor_mines'] = self._count_neighbors(row, col)

    def _count_neighbors(self, row, col):
        count = 0
        for r in range(max(0, row-1), min(self.rows, row+2)):
            for c in range(max(0, col-1), min(self.cols, col+2)):
                if self.grid[r][c]['is_mine']:
                    count += 1
        return count

    def reveal_cell(self, row, col):
        print(f"Revealing cell at ({row}, {col})")
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return "out_of_bounds"

        cell = self.grid[row][col]

        if cell['is_revealed']:
            return "already_revealed"
        
        cell['is_revealed'] = True

        if cell['is_mine']:
            return "mine"

        if cell['neighbor_mines'] == 0:
            self._flood_fill(row, col)

        return "safe"

    def _flood_fill(self, row, col):
        for delta_row in (-1, 0, 1):
            for delta_col in (-1, 0, 1):
                if delta_row == 0 and delta_col == 0:
                    continue

                neighbor_row, neighbor_col = row + delta_row, col + delta_col

                if 0 <= neighbor_row < self.rows and 0 <= neighbor_col < self.cols:
                    neighbor = self.grid[neighbor_row][neighbor_col]

                    if not neighbor['is_revealed'] and not neighbor['is_mine']:
                        neighbor['is_revealed'] = True

                        if neighbor['neighbor_mines'] == 0:
                            self._flood_fill(neighbor_row, neighbor_col)

    def place_mines_around_safe_cell(self, safe_row, safe_col):
        print(f"Placing mines around safe cell: ({safe_row}, {safe_col})")
        positions = set()
        excluded = set()

        for delta_row in (-1, 0, 1):
            for delta_col in (-1, 0, 1):
                row, col = safe_row + delta_row, safe_col + delta_col
                if 0 <= row < self.rows and 0 <= col < self.cols:
                    excluded.add((row, col))

        while len(positions) < self.mine_count:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if (row, col) not in excluded and not self.grid[row][col]['is_mine']:
                positions.add((row, col))

        for row, col in positions:
            self.grid[row][col]['is_mine'] = True

        self._calculate_neighbors()

    def check_win(self):
        for row in self.grid:
            for cell in row:
                if not cell['is_mine'] and not cell['is_revealed']:
                    return False
        return True

class GameLogic:
    def __init__(self, rows, cols, mine_count):
        self.grid = Grid(rows, cols, mine_count)
        self.mines_placed = False

    def place_mines(self, safe_row, safe_col):
        self.grid.place_mines(safe_row, safe_col)
        self.mines_placed = True

    def reveal_cell(self, row, col):
        print(f"Revealing cell at ({row}, {col})")

        if not self.mines_placed:
            print(f"Placing mines around cell ({row}, {col})...")
            self.place_mines(row, col)

        return self.grid.reveal_cell(row, col)

    def check_win(self):
        """Override check_win in GameComponent."""
        return self.grid.check_win()
