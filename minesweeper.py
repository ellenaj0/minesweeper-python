import tkinter as tk
from tkinter import messagebox
import random

GRID_SIZE = 9
MINES = 10


class Minesweeper:

    def __init__(self, window):
        self.window = window

        # Frame for the 9x9 grid with cells
        center_frame = tk.Frame(self.window, width=300, height=300, relief=tk.RIDGE, borderwidth=10, bg="gray")
        center_frame.pack()
        self.center_frame = center_frame
        self.all_cells = []

        # set up grid
        self.setup_grid()

    def setup_grid(self):

        # Create cells
        for x_coord in range(GRID_SIZE):
            new_row = []
            for y_coord in range(GRID_SIZE):
                cell = {"x": x_coord,
                        "y": y_coord,
                        "isMine": False,
                        "isOpened": False,
                        "isFlagged": False,
                        "button": tk.Button(self.center_frame, height=2, width=2, highlightthickness=0)
                        }

                cell["button"].bind("<Button-1>", self.left_click_wrapper(cell))
                cell["button"].bind("<Button-2>", self.right_click_wrapper(cell))

                cell["button"].grid(row=x_coord, column=y_coord, sticky="nsew")
                new_row.append(cell)
            self.all_cells.append(new_row)

    def determine_mines(self, cell):
        indices = [(row, col) for row in range(GRID_SIZE) for col in range(GRID_SIZE)]
        indices.remove((cell["x"], cell["y"]))
        mine_indices = random.sample(indices, MINES)
        for x_coord in range(GRID_SIZE):
            for y_coord in range(GRID_SIZE):
                if (x_coord, y_coord) in mine_indices:
                    self.all_cells[x_coord][y_coord]["isMine"] = True

    def get_neighboring_cells(self, cell) -> list:
        neighbors_coord = [(cell["x"] - 1, cell["y"] - 1),  # top left
                           (cell["x"] - 1, cell["y"]),      # top center
                           (cell["x"] - 1, cell["y"] + 1),  # top right
                           (cell["x"], cell["y"] - 1),      # left
                           (cell["x"], cell["y"] + 1),      # right
                           (cell["x"] + 1, cell["y"] - 1),  # bottom left
                           (cell["x"] + 1, cell["y"]),      # bottom center
                           (cell["x"] + 1, cell["y"] + 1)   # bottom right
                           ]
        neighbors = []

        for (x, y) in neighbors_coord:
            try:
                if x >= 0 and y >= 0:
                    neighbors.append(self.all_cells[x][y])
            except IndexError:
                pass
        return neighbors

    def right_click_wrapper(self, cell):
        return lambda event: self.right_click(cell)

    def left_click_wrapper(self, cell):
        return lambda event: self.left_click(cell)

    def right_click(self, cell):
        # already opened cell cannot be right-clicked
        if cell["isOpened"]:
            return

        # un-flag a cell
        if cell["isFlagged"]:
            cell["button"].configure(text="")
            cell["isFlagged"] = False
            return

        cell["button"].configure(text="F", fg="red")
        cell["isFlagged"] = True

    def left_click(self, cell):
        # determine mines after the first cell has been clicked to exclude the firstly clicked cell from the
        # mine selection indices
        if self.open_cells_count() == 0:
            self.determine_mines(cell)

        # flagged cells cannot be uncovered
        if cell["isFlagged"]:
            return

        # if uncovered cell is mine -> GAME OVER
        if cell["isMine"]:
            cell["button"].configure(text="M", fg="black")
            self.game_over()
            return

        else:
            self.open_cell(cell)
            if self.neighboring_mines_count(cell) == 0:
                self.uncover_surrounding_cells(cell, [cell])
            if self.open_cells_count() == (GRID_SIZE * GRID_SIZE) - MINES:
                self.win()  # last cell not opened??

    def neighboring_mines_count(self, cell) -> int:
        mines_count = 0
        neighbors = self.get_neighboring_cells(cell)
        for neighboring_cell in neighbors:
            if neighboring_cell["isMine"]:
                mines_count += 1
        return mines_count

    def open_cells_count(self):
        return len([cell for row in self.all_cells for cell in row if cell["isOpened"] is True])

    def open_cell(self, cell):
        cell["button"].configure(text=f"{self.neighboring_mines_count(cell)}", fg="green")
        cell["isOpened"] = True

        if cell["isFlagged"]:
            cell["isFlagged"] = False

        # after the cell has been opened, it can not be left-clicked anymore
        cell["button"].unbind("<Button-1>")
        cell["button"].unbind("<Button-2>")

    def uncover_surrounding_cells(self, cell, uncovered_list):
        for neighboring_cell in self.get_neighboring_cells(cell):
            if neighboring_cell["isMine"]:
                continue
            else:
                self.open_cell(neighboring_cell)
                if self.neighboring_mines_count(neighboring_cell) == 0 and (neighboring_cell not in uncovered_list):
                    uncovered_list.append(neighboring_cell)
                    self.uncover_surrounding_cells(neighboring_cell, uncovered_list)

    def win(self):
        answer = messagebox.askyesno("Congratulations", "You won! Restart game?")
        if answer:
            self.all_cells.clear()
            self.setup_grid()
        else:
            self.window.destroy()

    def game_over(self):

        answer = messagebox.askyesno("Game Over", "You pressed on a mine! Restart game?")
        if answer:
            self.all_cells.clear()
            self.setup_grid()
        else:
            self.window.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Minesweeper")
    minesweeper = Minesweeper(root)
    root.mainloop()
