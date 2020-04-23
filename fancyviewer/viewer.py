import tkinter
import time
from PIL import ImageTk, Image
import math
import os

import battlehack20
Team = battlehack20.game.team.Team


script_dir = os.path.dirname(__file__)

class FancyViewer(tkinter.Tk):
    def __init__(self, board_size, board_states, window_size=800):
        super().__init__()
        self.board_size = board_size
        self.board_states = board_states
        
        self.window_size = window_size
        self.square_size = self.window_size / self.board_size
        
        self.title("Battlehack 2020 -- Fancy Viewer")
        self.resizable(False, False)

        self.white_pawn = Image.open(os.path.join(script_dir, "images/white_pawn.png"))
        self.white_pawn = self.white_pawn.resize((int(self.square_size), int(self.square_size)), Image.ANTIALIAS)
        self.white_pawn = ImageTk.PhotoImage(self.white_pawn)

        self.black_pawn = Image.open(os.path.join(script_dir, "images/black_pawn.png"))
        self.black_pawn = self.black_pawn.resize((int(self.square_size), int(self.square_size)), Image.ANTIALIAS)
        self.black_pawn = ImageTk.PhotoImage(self.black_pawn)

        self.icon = Image.open(os.path.join(script_dir, "images/icon.png"))
        self.icon = ImageTk.PhotoImage(self.icon)
        self.iconphoto(True, self.icon)

        self.turn_slider = tkinter.Scale(self, from_=0, to=len(self.board_states)-1, orient=tkinter.HORIZONTAL, label="Turn", length=self.window_size - 60, command=self.update_index)
        self.turn_slider.pack(padx=20)
        
        stats_frame = tkinter.Frame(self)
        
        white_frame = tkinter.Frame(stats_frame)
        self.white_pawns = tkinter.IntVar()
        white_image = tkinter.Label(white_frame, image=self.white_pawn)
        white_image.pack(side=tkinter.LEFT)
        white_label = tkinter.Label(white_frame, textvariable=self.white_pawns)
        white_label.pack(side=tkinter.LEFT)
        white_frame.pack(side=tkinter.LEFT, padx=20)

        black_frame = tkinter.Frame(stats_frame)
        self.black_pawns = tkinter.IntVar()
        black_image = tkinter.Label(black_frame, image=self.black_pawn)
        black_image.pack(side=tkinter.LEFT)
        black_label = tkinter.Label(black_frame, textvariable=self.black_pawns)
        black_label.pack(side=tkinter.LEFT)
        black_frame.pack(side=tkinter.LEFT, padx=20)

        pause_button = tkinter.Button(stats_frame, text="Pause")
        pause_button.pack(side=tkinter.LEFT, padx=20)
        self.speed_slider = tkinter.Scale(stats_frame, from_=0, to=100, orient=tkinter.HORIZONTAL, label="Speed", length=self.window_size - 2*self.square_size - 250, command=self.update_speed)
        self.speed_slider.pack(side=tkinter.LEFT, padx=0)
        
        stats_frame.pack()
        
        self.canvas = tkinter.Canvas(self, width=self.window_size, height=self.window_size)
        self.squares = [
            [
                self.canvas.create_rectangle(
                    x * self.square_size,
                    y * self.square_size,
                    (x + 1) * self.square_size,
                    (y + 1) * self.square_size,
                    outline="",
                    fill="brown1" if (x^y)&1 else "white"
                ) for x in range(self.board_size)
            ] for y in range(self.board_size)
        ]
        self.canvas.pack()

        self.pawns = [[None for x in range(self.board_size)] for y in range(self.board_size)]
        self.old_board = [[None for x in range(self.board_size)] for y in range(self.board_size)]
        
        self.bind("<Right>", self.step)
        self.bind("<Left>", self.step_back)
        self.bind("<Up>", self.speed_up)
        self.bind("<Down>", self.slow_down)
        self.bind("p", self.pause)

        self.delay = None
        self.index = None
        self.paused = False
        self.min_delay = 0.02
        self.max_delay = 1
        self.run_time = 0
        self.last_time = time.time()
        
    def play(self, delay=0.5):
        self.delay = delay
        self.index = -1
        self.paused = False
        self.after(100, self.run)
        self.mainloop()

    def run(self):
        now = time.time()
        self.run_time += now - self.last_time
        self.last_time = now
        if self.run_time > self.delay:
            self.run_time %= self.delay
            if not self.paused:
                self.step()
        self.after(1, self.run)

    def pause(self, _=None):
        self.paused ^= True

    def step(self, _=None):
        if self.index < len(self.board_states) - 1:
            self.index += 1
            self.update()

    def step_back(self, _=None):
        if self.index > 0:
            self.index -= 1
            self.update()

    def speed_up(self, _=None):
        self.speed_slider.set(self.speed_slider.get() + 5)
    
    def slow_down(self, _=None):
        self.speed_slider.set(self.speed_slider.get() - 5)
                  
    def clear(self):
        self.canvas.delete("pawn")
        self.pawns = [[None for x in range(self.board_size)] for y in range(self.board_size)]
        self.old_board = [[None for x in range(self.board_size)] for y in range(self.board_size)]
    def view(self):
        board = self.board_states[self.index]
        
        for y in range(self.board_size):
            for x in range(self.board_size):
                if board[y][x]:
                    if self.old_board[y][x] and self.old_board[y][x].team == board[y][x].team:
                        continue
                    if self.old_board[y][x]:
                        self.canvas.delete(self.pawns[y][x])
                    image = self.white_pawn if board[y][x].team == Team.WHITE else self.black_pawn
                    
                    self.pawns[y][x] = self.canvas.create_image(
                        x * self.square_size,
                        (self.board_size - y) * self.square_size,
                        image=image,
                        tags="pawn",
                        anchor=tkinter.SW
                    )
                elif self.pawns[y][x]:
                    self.canvas.delete(self.pawns[y][x])
                    
        self.old_board = board

    def update_pawns(self):
        white_pawns = 0
        black_pawns = 0
        for row in self.board_states[self.index]:
            for square in row:
                if not square:
                    continue
                if square.team == Team.WHITE:
                    white_pawns += 1
                else:
                    black_pawns += 1
        self.white_pawns.set(white_pawns)
        self.black_pawns.set(black_pawns)

    def update_index(self, _=None):
        self.index = int(self.turn_slider.get())
        self.update()

    def update_speed(self, _=None):
        diff = math.log(self.max_delay / self.min_delay)
        val = diff * self.speed_slider.get() / 100
        self.delay = self.max_delay / math.pow(math.e, val)
        
    def update(self):
        self.view()
        self.update_pawns()
        self.turn_slider.set(self.index)
                    
