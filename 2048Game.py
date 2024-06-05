import tkinter as tk
import random
import json
import os

# Constants
SIZE = 4
WIN_TILE = 2048
BACKGROUND_COLOR = "#bbada0"
EMPTY_CELL_COLOR = "#cdc1b4"
TILE_COLORS = {
    2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563",
    32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72", 256: "#edcc61",
    512: "#edc850", 1024: "#edc53f", 2048: "#edc22e",
}
FONT = ("Verdana", 40, "bold")

class Game2048:
    def __init__(self, root):
        self.root = root
        self.board = [[0] * SIZE for _ in range(SIZE)]
        self.score = 0
        self.history = []
        self.init_gui()
        self.start_game()
    
    def init_gui(self):
        self.root.title("2048")
        self.root.bind("<Key>", self.key_handler)
        self.grid = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        self.grid.pack(fill=tk.BOTH, expand=True)
        self.cells = [[tk.Label(self.grid, bg=EMPTY_CELL_COLOR, font=FONT, width=4, height=2)
                       for _ in range(SIZE)] for _ in range(SIZE)]
        for i in range(SIZE):
            for j in range(SIZE):
                self.cells[i][j].grid(row=i, column=j, padx=5, pady=5)

        self.score_label = tk.Label(self.root, text="Score: 0", font=("Verdana", 24))
        self.score_label.pack()

        self.leaderboard = self.load_leaderboard()
        self.leaderboard_label = tk.Label(self.root, text="Leaderboard: \n" + "\n".join(self.leaderboard), font=("Verdana", 14))
        self.leaderboard_label.pack()

    def start_game(self):
        self.add_tile()
        self.add_tile()
        self.update_gui()
    
    def add_tile(self):
        empty_cells = [(i, j) for i in range(SIZE) for j in range(SIZE) if self.board[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.board[i][j] = random.choice([2, 4])
    
    def update_gui(self):
        for i in range(SIZE):
            for j in range(SIZE):
                value = self.board[i][j]
                if value == 0:
                    self.cells[i][j].config(text="", bg=EMPTY_CELL_COLOR)
                else:
                    self.cells[i][j].config(text=str(value), bg=TILE_COLORS.get(value, "#3c3a32"))
        self.score_label.config(text=f"Score: {self.score}")

    def move(self, direction):
        self.save_state()
        moved = False
        if direction == "up":
            for j in range(SIZE):
                col = [self.board[i][j] for i in range(SIZE)]
                new_col, score_add = self.merge(col)
                for i in range(SIZE):
                    if self.board[i][j] != new_col[i]:
                        moved = True
                    self.board[i][j] = new_col[i]
                self.score += score_add
        elif direction == "down":
            for j in range(SIZE):
                col = [self.board[i][j] for i in range(SIZE-1, -1, -1)]
                new_col, score_add = self.merge(col)
                for i in range(SIZE):
                    if self.board[SIZE-1-i][j] != new_col[i]:
                        moved = True
                    self.board[SIZE-1-i][j] = new_col[i]
                self.score += score_add
        elif direction == "left":
            for i in range(SIZE):
                row = self.board[i]
                new_row, score_add = self.merge(row)
                if self.board[i] != new_row:
                    moved = True
                self.board[i] = new_row
                self.score += score_add
        elif direction == "right":
            for i in range(SIZE):
                row = self.board[i][::-1]
                new_row, score_add = self.merge(row)
                new_row.reverse()
                if self.board[i] != new_row:
                    moved = True
                self.board[i] = new_row
                self.score += score_add
        
        if moved:
            self.add_tile()
            self.update_gui()
            if self.is_game_over():
                self.game_over()

    def merge(self, tiles):
        new_tiles = [tile for tile in tiles if tile != 0]
        score_add = 0
        for i in range(len(new_tiles) - 1):
            if new_tiles[i] == new_tiles[i + 1]:
                new_tiles[i] *= 2
                new_tiles[i + 1] = 0
                score_add += new_tiles[i]
        new_tiles = [tile for tile in new_tiles if tile != 0]
        new_tiles += [0] * (SIZE - len(new_tiles))
        return new_tiles, score_add

    def key_handler(self, event):
        key = event.keysym
        if key == "Up":
            self.move("up")
        elif key == "Down":
            self.move("down")
        elif key == "Left":
            self.move("left")
        elif key == "Right":
            self.move("right")
        elif key == "u":
            self.undo()

    def is_game_over(self):
        for i in range(SIZE):
            for j in range(SIZE):
                if self.board[i][j] == 0:
                    return False
                if i > 0 and self.board[i][j] == self.board[i-1][j]:
                    return False
                if i < SIZE-1 and self.board[i][j] == self.board[i+1][j]:
                    return False
                if j > 0 and self.board[i][j] == self.board[i][j-1]:
                    return False
                if j < SIZE-1 and self.board[i][j] == self.board[i][j+1]:
                    return False
        return True

    def game_over(self):
        self.save_score()
        tk.messagebox.showinfo("Game Over", f"Game Over! Your score: {self.score}")
        self.reset()

    def save_state(self):
        self.history.append((self.score, [row[:] for row in self.board]))

    def undo(self):
        if self.history:
            self.score, self.board = self.history.pop()
            self.update_gui()

    def reset(self):
        self.board = [[0] * SIZE for _ in range(SIZE)]
        self.score = 0
        self.history = []
        self.start_game()

    def save_score(self):
        self.leaderboard.append(f"Score: {self.score}")
        self.leaderboard = sorted(self.leaderboard, key=lambda x: int(x.split()[1]), reverse=True)[:5]
        with open("leaderboard.json", "w") as f:
            json.dump(self.leaderboard, f)

    def load_leaderboard(self):
        if os.path.exists("leaderboard.json"):
            with open("leaderboard.json", "r") as f:
                return json.load(f)
        return []

if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()