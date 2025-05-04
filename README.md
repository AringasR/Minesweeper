# Minesweeper Game Project

This project is a Python-based implementation of the classic **Minesweeper** game. The game allows players to uncover cells on a grid, flag potential mines, and attempt to clear the board without triggering any mines. The game provides a simple graphical user interface using **pygame**, and features include saving/loading game progress, flagging mines, and determining win/loss conditions.

## Technologies Used
- **Python**: The primary programming language.
- **pygame**: A library used for creating the graphical interface.
- **unittest**: A framework for writing unit tests to ensure functionality.

## Design and Implementation

### Object-Oriented Principles

1. **Polymorphism**: The game uses polymorphism in the button system by having the Button class inherit from the ButtonBase class. The ButtonBase class provides a general structure with methods like draw() and handle_event(), while the Button class overrides these methods to implement specific button behavior, such as handling hover effects, clicks, and drawing styles. This allows for flexibility in extending or modifying button functionality without affecting the rest of the code.
   
2. **Inheritance**: The Grid and GameLogic classes inherit from the GameComponent class, which provides a general check_win() method. In Grid, this method is overridden to implement the specific win condition for Minesweeper, where the game is won if all non-mine cells are revealed. GameLogic relies on Grid for the win condition, calling self.grid.check_win(). This use of inheritance allows for code reuse and facilitates extending the game with new components that follow a consistent structure.

3. **Abstraction**: The game uses abstract methods to define generic behaviors for different scenes (e.g., menu_scene.py, game_scene.py). This hides the complexity of each scene and provides a clear interface for switching between them.

4. **Encapsulation**: Private methods (denoted by a leading underscore) are used to encapsulate game logic that should not be accessed directly. For example, the _calculate_neighbors() method in the Grid class (from logic.py) calculates neighboring mines for each cell. It is kept private and used internally to manage the grid’s state, ensuring the game's logic remains hidden and preventing unnecessary complexity.

### Design Pattern Used: Factory:
While not fully formalized, a **Factory** Pattern is present in the game's menu system. The MainMenu class abstracts the creation of buttons through the setup_buttons() method. This method acts as a basic factory by handling the logic for creating and initializing multiple buttons, which promotes flexibility and potential extension in the future.

## Features Implemented

1. **Core Gameplay**: The player interacts with the grid by left-clicking or chord clicking (left + right click) to reveal a cell and right-clicking to flag a suspected mine. The game ends if the player reveals a mine, or if all non-mine cells are revealed.
   
2. **Save/Load Game**: The game allows players to save and load their progress using a file-based approach. The grid state, number of mines, and game-over status are saved to a file and can be restored later.
   
3. **Main and Pause Menus**: The main menu provides options to start a new game, load a saved game, or exit. The pause menu allows the player to resume the game or access other options like saving or quitting.

4. **Win/Loss Conditions**: The game detects a win when all non-mine cells are revealed. The game ends in a loss if the player reveals a mine.

## Testing

I wrote unit tests using Python's **unittest** framework to verify the correctness of critical game components.

### Unit Tests Implemented:

1. **Save/Load Game**: Tests to ensure that the game state (including the grid, flags, and revealed cells) is correctly saved and loaded.
2. **Cell Reveal**: Tests to check that cells are revealed correctly and that the game ends when a mine is revealed.
3. **Win/Loss Conditions**: Tests to verify that the game correctly detects when the player wins (all non-mine cells are revealed) or loses (a mine is revealed).

### Test Coverage:

- **Save/Load Functionality**: Ensured that all properties of the game state, including the grid, mines, flags, and revealed cells, are properly saved and restored.
- **Core Game Logic**: Verified that cells are revealed properly and that the game handles flagging and cell revealing correctly.

## Challenges and Solutions

### Challenges:

1. **State Management**: One of the major challenges was managing the game state during saving and loading. Ensuring that the state of each cell (revealed, flagged, etc.) was preserved required careful handling of the grid and game logic.

### Solutions:

1. **Using OOP Principles**: I used **encapsulation** to hide the internal details of each game component, such as the grid and the state of individual cells, while exposing necessary methods for saving and loading the game state.
2. **Unit Testing**: I wrote unit tests to ensure the correctness of the save/load functionality and game logic. This helped identify issues early in the development process.

## Conclusion

In this project, I successfully implemented a **Minesweeper game** using **OOP principles** and **design patterns**. The core functionality of the game, including cell revealing, flagging, saving, and loading, is working as expected. Unit tests were written to verify the correctness of the game logic and ensure that the game behaves as intended.

### Future Improvements:
1. **Custom Difficulty Level**: Implement an option for the player to make a custom map to play on.
2. **Graphical Enhancements**: Add animations or additional visual effects to enhance the user experience.
