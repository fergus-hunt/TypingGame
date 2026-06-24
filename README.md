# Pygame Typing Survival Game

An interactive, keyboard-driven typing game built in Python using **Pygame** for gameplay and **Tkinter** for configuration and statistics viewing.

The player must navigate their character through a checkpoint graph by typing randomly generated strings connecting adjacent nodes. Meanwhile, an enemy skeleton relentlessly pursues the player.

---

## 🚀 Key Features

*   **Real-time Pathfinding (Dijkstra's Algorithm)**: 
    *   The enemy uses a manual implementation of **Dijkstra's Shortest Path Algorithm** to dynamically recalculate the quickest path to the player's current checkpoint every time the player moves.
*   **Security & Safety**:
    *   **SQL Injection Protection**: All SQLite database interactions utilize parameterized queries (`?` placeholders) instead of string formatting.
    *   **Password Hashing**: User passwords are securely stored in the SQLite database (`app_data.db`) using SHA-256 hashes instead of plaintext.
*   **Highly Customizable Settings**:
    *   Adjust themes (colors), key press sound effects, background music, and typography styles directly from an in-game Tkinter configuration menu.
*   **Local High Score Leaderboard**:
    *   Logs performance stats (words-per-minute, errors, dates, scores) using SQLite, allowing users to view and compare their past stats.

---

## 🛠️ Architecture

*   **[main.py](pythonfiles/main.py)**: Central game state machine and execution loop.
*   **[typing_game.py](pythonfiles/typing_game.py)**: Manages main gameplay mechanics, round progressions, character movement, and enemy Dijkstra path recalculation.
*   **[game_entity.py](pythonfiles/game_entity.py)**: Base sprite class representing moving elements with left/right/forward animation framing.
*   **[database_manager.py](pythonfiles/database_manager.py)**: Handles connection initialization, user account creation, score logging, and query retrieval securely.
*   **[settings.py](pythonfiles/settings.py)**: GUI options menu built using Tkinter that saves options directly to JSON.

---

## 📥 Getting Started

### Prerequisites
*   Python 3.x
*   Pygame: `pip install pygame`

### Running the Game
Launch the game from the root directory:
```bash
python pythonfiles/main.py
```
