import time
import datetime
import tkinter
from PIL import ImageTk, Image
import os

import battlehack20
Team = battlehack20.game.team.Team


script_dir = os.path.dirname(__file__)

class FancyViewer:
    def __init__(self, board_size, board_states, window_size=800):        
        self.board_size = board_size
        self.board_states = board_states
        self.window = Window(board_size, square_size=window_size // self.board_size)        

    def play(self, delay=0.5):
        run_time = 0
        last_time = datetime.datetime.now().timestamp()
        for state_index in range(len(self.board_states)):
            while run_time < delay:
                now = datetime.datetime.now().timestamp()
                run_time += now - last_time
                last_time = now
                self.window.master.update() # Handle any events that occur
                time.sleep(0.01)
            
            run_time %= delay

            self.clear()
            self.view(state_index)
        
        while True:
            try:
                self.window.master.update()
            except:
                break
            time.sleep(0.01)

    def play_synchronized(self, poison_pill, delay=0.5):
        print('')
        
        state_index = 0
        run_time = 0
        last_time = datetime.datetime.now().timestamp()
        while state_index < len(self.board_states) or not poison_pill.is_set():
            while len(self.board_states) <= state_index or runtime < delay:
                now = datetime.datetime.now().timestamp()
                run_time += now - last_time
                last_time = now
                self.window.master.update() # Handle any events that occur
                time.sleep(0.01)

            run_time %= delay

            self.clear()
            self.view(state_index)
            state_index += 1

        while True:
            try:
                self.window.master.update()
            except:
                break
            time.sleep(0.01)
          
    def clear(self):
        self.window.clear()
    
    def view(self, index=-1):
        self.window.view(self.board_states[index])

class Window:
    def __init__(self, board_size, square_size=50):
        self.board_size = board_size
        self.square_size = square_size
        self.size = self.board_size * self.square_size
        
        self.master = tkinter.Tk()

        self.canvas = tkinter.Canvas(self.master, width=self.size, height=self.size)
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

        self.images = []

        self.white_pawn = Image.open(os.path.join(script_dir, "images/white_pawn.png"))
        self.white_pawn = self.white_pawn.resize((self.square_size, self.square_size), Image.ANTIALIAS)
        self.white_pawn = ImageTk.PhotoImage(self.white_pawn)

        self.black_pawn = Image.open(os.path.join(script_dir, "./images/black_pawn.png"))
        self.black_pawn = self.black_pawn.resize((self.square_size, self.square_size), Image.ANTIALIAS)
        self.black_pawn = ImageTk.PhotoImage(self.black_pawn)


    def clear(self):
        self.canvas.delete("pawn")

    def view(self, board):
        for y in range(self.board_size):
            for x in range(self.board_size):
                if board[y][x]:
                    image = self.white_pawn if board[y][x].team == Team.WHITE else self.black_pawn
                    self.images.append(
                        self.canvas.create_image(
                            x * self.square_size,
                            (self.board_size - y) * self.square_size,
                            image=image,
                            tags="pawn",
                            anchor=tkinter.SW
                            )
                        )
        self.master.update()
                    
