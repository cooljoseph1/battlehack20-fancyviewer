This repository contains the code for the Battlehack20 fancyviewer.

## Installation and Usage

### Installation
To install the viewer, run
```bash
$ pip install battlehack20-fancyviewer
```

### Usage
You can then edit `run.py` in your battlehack20-scaffold to use this viewer as follows:
```python
from fancyviewer import FancyViewer
...
if __name__ == "__main__":
    ...
    viewer = FancyViewer(args.board_size, game.board_states)
```

You can also run a game from a log file in the following way:
```bash
$ python -m fancyviewer [log_file]
```
