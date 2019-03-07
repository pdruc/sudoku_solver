import pandas as pd
import numpy as np
import math

DEFAULT_PATH = 'easy_board.csv'


class Puzzle:
    def __init__(self, puzzle_size=9, puzzle_path=DEFAULT_PATH):
        self.puzzle_size = puzzle_size
        self.puzzle_path = puzzle_path

        self.puzzle = np.array(pd.read_csv(self.puzzle_path, header=None))
        self.fabric_rows_columns = None
        self.get_fabric_values_indexes()

    def get_fabric_values_indexes(self):
        rows, columns = np.where(self.puzzle != 0)
        self.fabric_rows_columns = set([(r, c) for r, c in zip(rows, columns)])

    def reshape_to_1d(self, array):
        return np.reshape(array, self.puzzle_size ** 2)

    @staticmethod
    def get_row_values(i, puzzle):
        return puzzle[i, :]

    @staticmethod
    def get_col_values(i, puzzle):
        return puzzle[:, i]

    def get_block_values(self, i, j, puzzle):
        block_center_x = int(3 * (i // math.sqrt(self.puzzle_size)) + 1)
        block_center_y = int(3 * (j // math.sqrt(self.puzzle_size)) + 1)
        return puzzle[block_center_x-1:block_center_x+2, block_center_y-1:block_center_y+2]


class Solver(Puzzle):
    def __init__(self):
        Puzzle.__init__(self)

        self.full_set = set(range(1, self.puzzle_size + 1))
        self.possible_values = list([[set() for _ in range(self.puzzle_size)] for _ in range(self.puzzle_size)])

        self.solved_values = np.zeros_like(self.puzzle, dtype=int)
        self.possible_values_count = np.zeros_like(self.puzzle, dtype=int)
        self.solved_rows_columns = set().union(self.fabric_rows_columns)

    def solve_step(self):
        """Make one step in solving sudoku!

        Steps made in one step:
        1. Compute possible values for all cells in the puzzle.
        2. Check for cells with only one possible value and solve them
        3. If any such cells were found finish function's execution.
        4. If not, select all cells with minimum number of possible values.
        5.
         """
        for i in range(0, self.puzzle_size):
            for j in range(0, self.puzzle_size):
                if (i, j) not in self.solved_rows_columns:
                    self.possible_values[i][j] = self.get_possible_values(i, j, self.puzzle + self.solved_values)
                    self.possible_values_count[i, j] = len(self.possible_values[i][j])
                else:
                    self.possible_values[i][j] = set()

        rows_solvable, cols_solvable = np.where(self.possible_values_count == 1)
        solvable_rows_columns = set([(r, c) for r, c in zip(rows_solvable, cols_solvable)])

        if solvable_rows_columns:
            for coords in solvable_rows_columns:
                i, j = coords
                self.solved_values[i, j] = list(self.possible_values[i][j])[0]
                self.solved_rows_columns.update([(i, j)])
                self.possible_values_count[i, j] = 0

            return None

        else:
            rows_to_care, cols_to_care = np.where(self.possible_values_count == np.amin(self.possible_values_count))
            to_care = set([(r, c) for r, c in zip(rows_to_care, cols_to_care)])

            # for coords in to_care:
            #     i, j = coords
            #     self.pseudo_solved_values[i, j] = list(self.possible_values[i][j])[0]

    def get_possible_values(self, i, j, puzzle):
        possible_values = self.full_set
        possible_values = possible_values.difference(self.get_row_values(i, puzzle).ravel())
        possible_values = possible_values.difference(self.get_col_values(j, puzzle).ravel())
        possible_values = possible_values.difference(self.get_block_values(i, j, puzzle).ravel())

        return possible_values


def main():
    pass


if __name__ == '__main__':
    main()
