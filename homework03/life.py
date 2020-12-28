import pathlib
import random
import typing as tp
import copy

Cell = tp.Tuple[int, int]
CellsArray = tp.List[int]
Grid = tp.List[CellsArray]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size

        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()

        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)

        # Максимальное число поколений
        self.max_generations = max_generations

        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize=False):
        grid = []

        for row in range(self.rows):
            grid.append([])
            for col in range(self.cols):
                if randomize:
                    is_alive = random.choice([0, 1])
                else:
                    is_alive = 0

                grid[row].append(is_alive)

        return grid

    def get_neighbours(self, cell: Cell) -> CellsArray:
        cell_row, cell_col = cell
        neighbours = []

        for row in range(cell_row - 1, cell_row + 2):
            for col in range(cell_col - 1, cell_col + 2):
                if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
                    continue

                if row == cell_row and col == cell_col:
                    continue

                is_alive = self.curr_generation[row][col]
                neighbours.append(is_alive)

        return neighbours

    def get_next_generation(self) -> Grid:
        new_grid = copy.deepcopy(self.curr_generation)

        for row in range(self.rows):
            for col in range(self.cols):
                neighbours = self.get_neighbours((row, col))
                is_alive = self.curr_generation[row][col]

                if sum(neighbours) in [2, 3] and is_alive == 1:
                    pass

                elif sum(neighbours) == 3:
                    new_grid[row][col] = 1

                else:
                    new_grid[row][col] = 0

        return new_grid

    def step(self) -> None:
        if self.generations > self.max_generations:
            return

        self.prev_generation = copy.deepcopy(self.curr_generation)
        self.curr_generation = self.get_next_generation()

        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        if self.generations >= self.max_generations:
            return True
        else:
            return False

    @property
    def is_changing(self) -> bool:
        was_changed = False

        for row in range(self.rows):
            for col in range(self.cols):
                if self.prev_generation[row][col] != self.curr_generation[row][col]:
                    was_changed = True
                    break

        return was_changed

    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        file = filename.read_text().split('\n')
        file.remove('')

        grid = []
        for line in file:
            grid.append(list(map(int, line)))

        game = GameOfLife((len(grid), len(grid[0])), False)
        game.curr_generation = grid

        return game

    def save(self, filename: pathlib.Path) -> None:
        pass
