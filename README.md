# Teeko AI Player

This project is an intelligent AI agent that plays the board game Teeko. The AI uses the **Minimax algorithm** with a depth-limited search and a heuristic evaluation function to make strategic moves against a human player.

[cite_start]This was developed as a project to practice game theory, AI algorithms, and Python software design[cite: 1, 2, 3].

---

## 🎮 Game Rules

[cite_start]Teeko is a two-player abstract strategy game played on a 5x5 board[cite: 12].

* [cite_start]**Players**: Each player has four markers[cite: 13].
* [cite_start]**Drop Phase**: Players take turns placing their four markers on any empty space on the board[cite: 14].
* [cite_start]**Move Phase**: Once all eight markers are on the board, players take turns moving one of their pieces to an adjacent empty space (horizontally, vertically, or diagonally)[cite: 15].
* [cite_start]**Win Conditions**: The first player to achieve one of the following wins the game[cite: 20]:
    * [cite_start]Four markers in a straight line (horizontal, vertical, or diagonal)[cite: 21].
    * [cite_start]Four markers in a 2x2 square[cite: 22].

---

## ✨ Features

* **Intelligent AI**: Play against an AI powered by the Minimax algorithm.
* **Heuristic Evaluation**: The AI evaluates non-winning board positions to make strategically sound moves.
* **Interactive CLI**: A clean and responsive command-line interface for gameplay.
* **Input Validation**: Robust error handling for user input to prevent crashes and guide the player.
* **Built-in Instructions**: A help menu to explain the rules to new players.

---

## 🚀 How to Run

1.  Ensure you have **Python 3.x** installed.
2.  Clone this repository to your local machine.
3.  Navigate to the project directory in your terminal.
4.  Run the game with the following command:
    ```sh
    python game.py
    ```
5.  Follow the on-screen prompts to play! You will be asked if you want to see the instructions before the game begins.

---

## 📂 File Structure

* `game.py`: The main script containing the game logic, AI implementation, and user interface.
