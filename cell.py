import tkinter as tk

# change
class Cell:

    def __init__(self, x, y, frame):
        self.x = x
        self.y = y
        self.frame = frame
        self.is_mine = False
        self.is_flagged = False
        self.is_opened = False

        # create button
        cell_btn = tk.Button(frame, height=2, width=2)
        cell_btn.bind("<Button-1>", self.left_click)
        cell_btn.bind("<Button-2>", self.right_click)
        self.button = cell_btn
        # NOTE: For windows "<Button-3>" for right click

    # what happens when mouse it left-clicked
    def left_click(self, event):
        event.widget.configure(text="O", fg="green")
        self.is_opened = True
        print("Left button was clicked!")

    # what happens when mouse it right-clicked
    def right_click(self, event):
        event.widget.configure(text="F", fg="red")
        self.is_flagged = True
        print("Right button was clicked!")

