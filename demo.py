from itertools import dropwhile
import logging
import tkinter
from tkinter import Button, Entry, Frame, Label, PhotoImage, StringVar, ttk
from typing import Optional, Tuple
from PIL import Image, ImageTk
from pipes_v2.agent import demo_search

from pipes_v2.board import Board
from pipes_v2.joint import Joint
from pipes_v2.state import State
from pipes_v2.utils.generate import generate_board
from pipes_v2.utils.image_proc import download_board

BUTTON_SIZE = 17


class App(Frame):
    def __init__(self, root: tkinter.Tk) -> None:
        super().__init__(root)
        root.title("Pipes Solver Demo")
        self.config(pady=10)
        # board = download_board(
        #     "https://www.puzzle-pipes.com/screenshots/955da4475ec844fc32b1a71f0253cc26624125d20a8c3.png",
        #     15,
        #     15,
        # )
        logging.basicConfig(level=logging.INFO)
        Label(self, text="Pipes Solver", font="Courier 18 bold").pack()
        self.height_var = StringVar()
        self.height_var.set("10")
        Label(self, text="Enter height:").pack()
        Entry(self, textvariable=self.height_var).pack()

        self.width_var = StringVar()
        self.width_var.set("10")
        Label(self, text="Enter width").pack()
        Entry(self, textvariable=self.width_var).pack()

        self.generate_button = Button(self, text="Generate", command=self.generate)
        self.generate_button.pack()
        self.state_label = Label(self)
        self.state_label.pack()
        self.state_widget = None

        button_row = Frame(self)
        button_row.pack()

        self.button = Button(button_row, text="Next", command=self.next_state)
        self.button.pack(side="left")
        self.fast_button = Button(
            button_row, text="Fast Forward", command=self.fast_forward
        )
        self.fast_button.pack(side="left")
        self.finish_button = Button(
            button_row, text="Show Solution", command=self.finish
        )
        self.finish_button.pack(side="left")

    def generate(self):
        height = int(self.height_var.get())
        width = int(self.width_var.get())
        board = generate_board(height, width)
        self.state_gen = demo_search(board)
        if self.state_widget is not None:
            self.state_widget.destroy()
        self.state_widget = StateWidget(self, board, self.state_label)
        self.next_state()
        self.state_widget.pack()
        self.button.config(state="normal")
        self.fast_button.config(state="normal")
        self.finish_button.config(state="normal")

    def next_state(self):
        try:
            if self.state_widget is not None:
                self.state_widget.update_state(*next(self.state_gen))
        except StopIteration:
            self.button.config(state="disabled")
            self.fast_button.config(state="disabled")
            self.finish_button.config(state="disabled")

    def fast_forward(self):
        new_gen = dropwhile(lambda tup: tup[1][2].startswith("Try"), self.state_gen)
        try:
            if self.state_widget is not None:
                self.state_widget.update_state(*next(new_gen))
        except StopIteration:
            self.button.config(state="disabled")
            self.fast_button.config(state="disabled")
            self.finish_button.config(state="disabled")

    def finish(self):
        new_gen = dropwhile(lambda tup: tup[1][2] != "Solved", self.state_gen)
        if self.state_widget is not None:
            self.state_widget.update_state(*next(new_gen))
        self.button.config(state="disabled")
        self.fast_button.config(state="disabled")
        self.finish_button.config(state="disabled")


class StateWidget(tkinter.Frame):
    indices = {
        "1": 8,
        "2a": 12,
        "2b": 10,
        "3": 14,
    }

    def __init__(self, master, board: Board, label) -> None:
        super().__init__(master)
        self.board = board
        self.label = label
        self.pipe_widgets = [
            [
                Label(self, text=board.at(col, row).value)
                for col in range(0, board.WIDTH)
            ]
            for row in range(0, board.HEIGHT)
        ]
        for row in range(0, board.HEIGHT):
            for col in range(0, board.WIDTH):
                self.pipe_widgets[row][col].grid(column=col, row=row + 1)

    def update_state(
        self, state: State, status: Tuple[Optional[int], Optional[int], str]
    ):
        for y in range(0, self.board.HEIGHT):
            for x in range(0, self.board.WIDTH):
                config = state.joints.at(x, y)
                if any(map(Joint.is_unknown, config.joints())):
                    index = StateWidget.indices[self.board.at(x, y).value]
                    self.pipe_widgets[y][x].config(
                        image=photo_images[index], background="white"
                    )
                else:
                    index = sum(2 ** (3 - i) for i in range(0, 4) if config[i])
                    self.pipe_widgets[y][x].config(
                        image=photo_images[index], background="gray"
                    )
        current_x, current_y, statuscode = status
        if current_x is not None and current_y is not None:
            self.pipe_widgets[current_y][current_x].config(background="blue")
        self.label.config(text=statuscode)


if __name__ == "__main__":
    root = tkinter.Tk()
    global photo_images
    photo_images = [
        ImageTk.PhotoImage(
            Image.open("./pipes-maker/static/pipe-{}.png".format(i))
            .resize((BUTTON_SIZE, BUTTON_SIZE))
            .convert("RGBA")
        )
        for i in range(0, 15)
    ]
    App(root).pack(side="top", fill="both")
    root.mainloop()
