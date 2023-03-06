import tkinter as tk
from tkmacosx import Button
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
        # Todo: find a better way to do this
        indices = [(row, col) for row in range(GRID_SIZE) for col in range(GRID_SIZE)]
        mine_indices = random.sample(indices, MINES)
        print(mine_indices)

        # Create cells with randomized mines
        for x_coord in range(GRID_SIZE):
            new_row = []
            for y_coord in range(GRID_SIZE):
                cell = {"x": x_coord,
                        "y": y_coord,
                        "isMine": False,
                        "isOpened": False,
                        "isFlagged": False,
                        "button": tk.Button(self.center_frame, height=2, width=2)
                        }

                # to be updated - start
                if (x_coord, y_coord) in mine_indices:
                    cell["isMine"] = True
                # to be updated - end

                cell["button"].bind("<Button-1>", self.left_click_wrapper(cell))
                cell["button"].bind("<Button-2>", self.right_click_wrapper(cell))

                # NOTE: For windows "<Button-3>" for right click

                cell["button"].grid(row=x_coord, column=y_coord)
                new_row.append(cell)
            self.all_cells.append(new_row)

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

        # Todo: find better way to do this
        for (x, y) in neighbors_coord:
            try:
                if x != -1 and y != -1:
                    neighbors.append(self.all_cells[x][y])
            except IndexError:  # why do I need to catch this exception?
                pass
        return neighbors

    def right_click_wrapper(self, cell):
        return lambda event: self.right_click(cell)

    def left_click_wrapper(self, cell):
        return lambda event: self.left_click(cell)

    # what happens when the mouse if right-clicked
    def right_click(self, cell):
        # print("right button clicked")
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

    # what happens when mouse it left-clicked
    def left_click(self, cell):
        # print("left button clicked")
        # flagged cells cannot be uncovered
        if cell["isFlagged"]:
            return

        # if uncovered cell is mine -> GAME OVER
        if cell["isMine"]:
            cell["button"].configure(text="M", fg="black")
            return

        else:
            cell["button"].configure(text=f"{self.neighboring_mines_count(cell)}", fg="green")
            cell["isOpened"] = True

            # after the cell has been uncovered, it can not be left-clicked anymore
            cell["button"].unbind("<Button-1>")
            cell["button"].unbind("<Button-2>")

    def neighboring_mines_count(self, cell) -> int:
        mines_count = 0
        neighbors = self.get_neighboring_cells(cell)
        for neighboring_cell in neighbors:
            if neighboring_cell["isMine"]:
                mines_count += 1

        return mines_count

    def uncover_surrounding_cells(self, cell):
        pass

    def game_over(self):
        pass


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Minesweeper")
    # root.geometry("300x300")
    minesweeper = Minesweeper(root)

    root.mainloop()


