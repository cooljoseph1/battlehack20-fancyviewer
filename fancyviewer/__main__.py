"""
Run a game from a log output
"""
import sys
import argparse
from .viewer import FancyViewer

import battlehack20
Team = battlehack20.game.team.Team

class Robot:
    def __init__(self, team, id):
        self.team = team
        self.id = id

def parse_board(board):
    rows = board.split("\n")
    def parse_piece(piece):
        if piece == "[    ] ":
            return None
        team = Team.WHITE if piece[1] == "W" else Team.BLACK
        id = int(piece[3:5])
        return Robot(team, id)
    
    def parse_row(row):
        pieces = []
        for c in row:
            if c == "[":
                pieces.append([None, ""])
            elif c in ("B", "W"):
                pieces[-1][0] = Team.WHITE if c == "W" else Team.BLACK
            elif c in "0123456789":
                pieces[-1][1] += c
            elif c == "]":
                pieces[-1][1] = int(pieces[-1][1]) if pieces[-1][1] else None
        
        return [Robot(team, id) if team else None for team, id in pieces]
    
    return [parse_row(row) for row in rows]

def parse_logs(logs):
    board_states = logs.split("\n\n")
    board_states = [parse_board(board) for board in board_states[2:-2]]
    return board_states
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help="Path to log file.")
    parser.add_argument('--window-size', default=800, type=int, help="Override the window size of the viewer.")
    parser.add_argument('--delay', default=0.5, type=float, help="Override the delay size of the viewer.")
    args = parser.parse_args()
    
    with open(args.file) as f:
        logs = f.read()
    board_states = parse_logs(logs)
    board_size = len(board_states[0][0])

    viewer = FancyViewer(board_size, board_states, window_size=args.window_size)
    viewer.play(delay=args.delay)
    
    
    
