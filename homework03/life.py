import pathlib
import random
from random import randint
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


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
        self.curr_generation = self.prev_generation
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.n_generation = 1

    def create_grid(self, randomize=True, grid = []) -> Grid:
        
        if randomize:
            grid = [[random.randint(0, 1) for _ in range(self.cols)] for _ in range(self.rows)]
        else:
            grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
            
        return grid


    def get_neighbours(self, cell: Cell) -> Cells:

        x, y = cell
        neighbour = []
        for row in [-1, 0, 1]:
            for col in [-1, 0, 1]:
                if(
                        (row, col) != (0, 0) and
                        0 <= x + row < self.rows and
                        0 <= y + col < self.cols
                ):
                    neighbour.append(self.curr_generation[x + row][y + col])

        return neighbour

    def get_next_generation(self) -> Grid:
        
        self.next_generation = self.create_grid(randomize=False)
        for x in range(self.rows):
            for y in range(self.cols):
                yep_neighbour = self.get_neighbours((x, y)).count(1)
                if self.curr_generation[x][y] == 1 and yep_neighbour in [2, 3]:
                    self.next_generation[x][y] = 1
                elif self.curr_generation[x][y] == 0 and yep_neighbour == 3:
                    self.next_generation[x][y] = 1
                else:
                    self.next_generation[x][y] = 0
                    
        return self.next_generation

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.n_generation += 1

    @property
    def is_max_generations_exceed(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        
        return self.n_generation == self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        
        grid = []
        file = filename.open(mode="r")
        for line in file.readlines():
            line = line.replace("\n", "")
            row = []
            for char in line:
                row.append(int(char))
            grid.append(row)

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        
        file = filename.open(mode="w")
        for row in self.curr_generation:
            file.write("".join([str(char) for char in row]))
            file.write("\n")
