# Conway's Game of Life

This is a Python implementation of Conway's Game of Life using the Pygame library. The Game of Life is a cellular automaton devised by mathematician John Conway, where cells evolve based on simple rules.

## Features

- Create a grid of cells on a canvas.
- Customize grid size and cell colors.
- Initialize the grid randomly or by drawing on it.
- Simulate the evolution of cells based on the rules of the Game of Life.

## Prerequisites

Before running the code, make sure you have the following installed:

- Python (version 3.x)
- `pygame` library

## Installation

1. Clone this repository to your local machine.
2. Install the required Python packages.

## Usage

1. Open the `config.txt` file and customize the game settings (canvas size, colors, etc.) if needed.
2. Run the script (`main.py`) to start the Game of Life simulation.
3. You can interact with the grid using your mouse. Click to toggle cells between alive and dead, or use the `Enter` key to randomize the grid.
4. Press the `Space` key to pause or resume simulation. When the simulation is paused you can alter the grid as described above.
5. Use the `↑` and `↓` keys to change the simulation speed. The speed multiplier is shown above the grid.
6. Press the `Backspace` key to clear the grid.

## How It Works

The Game of Life operates on a grid of cells, each of which can be either alive or dead. The evolution of the grid is determined by the number of live neighbors each cell has:

- A live cell with 2 or 3 live neighbors survives.
- A dead cell with exactly 3 live neighbors becomes alive.
- All other cells die or remain dead.

The simulation continues iteratively, applying these rules to each cell in the grid.




