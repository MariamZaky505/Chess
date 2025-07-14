# ♟️ Chess AI Project

A graphical Chess game with an AI opponent built using Python and Pygame. The AI leverages the Minimax algorithm with Alpha-Beta Pruning, making it capable of playing against humans in real-time. This project was developed as an academic demonstration of game theory, search algorithms, and GUI development.

---

## 📌 Features

### 🎮 Game Interface
- Playable chess game using Pygame
- Human vs AI gameplay
- Five switchable board themes (press 1–5)
- Move highlighting and animations
- Support for special rules:
  - Castling
  - En Passant
  - Pawn Promotion (default to Queen)
- Undo move functionality (`U` key)
- Move log panel on the side
- Checkmate and stalemate detection

### 🧠 Artificial Intelligence
- **Minimax Algorithm** with **Alpha-Beta Pruning**
- Scoring system based on material and positional heuristics
- Adjustable search depth
- Random fallback move selection
- Efficient multiprocessing for AI thinking

---

## 🗂️ File Structure

| File          | Description |
|---------------|-------------|
| `ChessMain.py` | Main game loop, user input, and GUI rendering |
| `ChessEngine.py` | Handles board state, move validation, special moves |
| `AiChess.py`  | AI logic and decision-making algorithms |
| `images/`     | Folder containing all chess piece images (e.g., `wP.png`, `bK.png`) |

---

## 🧠 AI Algorithm Details

- **Minimax** explores all possible moves up to a fixed depth and evaluates them using heuristics.
- **Alpha-Beta Pruning** reduces computation by skipping branches that won't affect the final decision.
- **Positional Evaluation** enhances scoring based on piece location on the board.
- **Limitations**:
  - Fixed-depth search may miss long-term strategies
  - No advanced tactics (e.g., forks, pins) beyond basic heuristics

---

## 🛠️ Installation & Running

### Prerequisites
- Python 3.x
- Pygame

### Setup
```bash
pip install pygame
