import tkinter as tk
from cell import Cell
from tkmacosx import Button
from tkinter import messagebox
import random


GRID_SIZE = 9
MINES = 10


class Minesweeper:

    def __init__(self, window):
        self.window = window
        # Frame with the 9x9 grid
        center_frame = tk.Frame(master=self.window, width=300, height=300, relief=tk.RIDGE, borderwidth=10, bg="gray")
        center_frame.pack()
        self.center_frame = center_frame
        self.all_cells = []
        # Create buttons for each cell
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                cell = Cell(x=i, y=j, frame=center_frame)
                cell.button.grid(row=i, column=j)
                self.all_cells.append(cell)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Minesweeper")
    # window.geometry("300x300")
    minesweeper = Minesweeper(root)

    root.mainloop()

