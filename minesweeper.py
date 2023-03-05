import tkinter as tk
from cell import Cell
from tkmacosx import Button
from tkinter import messagebox
import random

GRID_SIZE = 9
MINES = 10

window = tk.Tk()
window.title("Minesweeper")
# window.geometry("300x300")

# Frame with the 9x9 grid
center_frame = tk.Frame(master=window, width=300, height=300, relief=tk.RIDGE, borderwidth=10, bg="gray")
center_frame.pack()

# Create buttons for each cell
for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
        cell = Cell(x=i, y=j, frame=center_frame)
        cell.button.grid(row=i, column=j)


window.mainloop()
