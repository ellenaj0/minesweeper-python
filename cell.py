import tkinter as tk

class Cell:

    def __init__(self, x, y, frame):
        self.x = x
        self.y = y
        self.frame = frame
        self.is_mine = False
        self.is_flagged = False
        self.is_opened = False
        self.neighboring_mines = 0

        # create button
        cell_btn = tk.Button(frame, height=2, width=2)
        cell_btn.bind("<Button-1>", self.left_click)
        cell_btn.bind("<Button-2>", self.right_click)
        self.button = cell_btn
        # NOTE: For windows "<Button-3>" for right click

    # what happens when mouse is left-clicked
    def left_click(self, event):

        # already opened cells or flagged cells cannot be left-clicked
        if self.is_opened or self.is_flagged:
            return

        # is uncovered cell is mine -> GAME OVER
        if self.is_mine:
            event.widget.configure(text="F", fg="black")
            return

        event.widget.configure(text="O", fg="green")
        self.is_opened = True

    # what happens when mouse is right-clicked
    def right_click(self, event):

        # already opened cell cannot be right-clicked
        if self.is_opened:
            return

        # un-flag a cell
        if self.is_flagged:
            event.widget.configure(text="")
            self.is_flagged = False
            return
        event.widget.configure(text="F", fg="red")
        self.is_flagged = True
