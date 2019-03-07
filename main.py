import math
from os import listdir

from kivy.app import App
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rectangle
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.clock import Clock

import solver

# Global variables
RESOLUTION = 512
REFRESH_RATE = 1

# Global app's properties
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', str(RESOLUTION))
Config.set('graphics', 'height', str(RESOLUTION))
Config.set('graphics', 'fullscreen', '0')

# Loading all sub .kv files from kv directory - NOT USED AT THE MOMENT
kv_path = './kv/'
for kv in listdir(kv_path):
    Builder.load_file(kv_path + kv)

# Loading main .kv file
Builder.load_file('main.kv')


class Board(GridLayout):
    def __init__(self, sudoku_size=9, thin_border_width=1, thick_border_width=5):
        """Make an instance of the Board class.

        Steps that are made:
        1. Memory for cells, borders and their properties (positions and sizes) is allocated.
        2. Cells and borders are defined.
        3. Position and size of a border are hooked into kivy’s event system.
        4. The puzzle (sudoku numbers) are loaded into the one of board's properties.
        """
        GridLayout.__init__(self)
        self.sudoku_size = sudoku_size
        self.cells = [None] * self.sudoku_size ** 2
        self.borders = [None] * 2 * (self.sudoku_size + 1)
        self.borders_positions = [tuple()] * 2 * (self.sudoku_size + 1)
        self.borders_sizes = [tuple()] * 2 * (self.sudoku_size + 1)

        self.thin = thin_border_width
        self.thick = thick_border_width

        self.define_cells()
        self.define_borders()
        self.bind(pos=self.update_layout, size=self.update_layout)

        self.puzzle = solver.Solver()

    def update_layout(self, *args):
        """Update borders positions and sizes according to the board's properties."""
        _ = args

        self.borders_positions[:self.sudoku_size + 1] = \
            [(i / self.sudoku_size * (self.width - self.thick), 0) for i in range(self.sudoku_size + 1)]
        self.borders_positions[self.sudoku_size + 1:] = \
            [(0, i / self.sudoku_size * (self.width - self.thick)) for i in range(self.sudoku_size + 1)]

        for i in range(self.sudoku_size + 1):
            self.borders_sizes[i] = (self.thin, self.height)
            self.borders_sizes[self.sudoku_size + 1 + i] = (self.width, self.thin)

        for i in range(0, self.sudoku_size + 1, int(math.sqrt(self.sudoku_size))):
            self.borders_sizes[i] = (self.thick, self.height)
            self.borders_sizes[self.sudoku_size + 1 + i] = (self.width, self.thick)

        with self.canvas:
            for i in range(len(self.borders)):
                self.borders[i].pos = self.borders_positions[i]
                self.borders[i].size = self.borders_sizes[i]

    def define_cells(self):
        """Define cells as Label() objects and add them to the board"""
        self.cells = []
        for i in range(self.sudoku_size ** 2):
            self.cells.append(Label(text=str(i)))
            self.add_widget(self.cells[i])

    def define_borders(self):
        """Define borders without any specific properties.

        Borders are defined before the board's position and size are set, so setting their positions and sizes is made
        in update_layout() method.
        """
        with self.canvas:
            self.borders = [Rectangle() for _ in self.borders]

    def update(self, dt):
        """Update cells values according to values from Puzzle() object

        0 means empty so zeros are omitted.
        """
        _ = dt

        self.puzzle.solve_step()

        puzzle = self.puzzle.reshape_to_1d(self.puzzle.puzzle)
        found_values = self.puzzle.reshape_to_1d(self.puzzle.solved_values)
        for i, c in enumerate(self.cells):
            if puzzle[i] != 0:
                c.text = str(puzzle[i])
            elif found_values[i] != 0:
                c.text = str(found_values[i])
                c.color = [0, 1, 0.4, 1]
            else:
                c.text = ''

        if all([c.text for c in self.cells]):
            for c in self.cells:
                c.color = [0, 1, 0.4, 1]


class Sudoku(App):
    def build(self):
        self.title = 'Sudoku solver'
        board = Board()
        Clock.schedule_interval(board.update, REFRESH_RATE)
        return board


if __name__ == '__main__':
    sudoku = Sudoku()
    sudoku.run()
