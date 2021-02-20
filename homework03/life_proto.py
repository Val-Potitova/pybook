import random
from random import randint
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

        self.grid = self.create_grid()

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        self.grid = self.create_grid(True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_lines()
            self.draw_grid()
            self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


        def create_grid(self, randomize: bool = True, grid=[]):
        """
        Создание списка клеток.
        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.
        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.
        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        
        if randomize:
            grid = [[random.randint(0, 1) for _ in range(self.cell_width)] for _ in range(self.cell_height)]
        else:
            grid = [[0 for _ in range(self.cell_width)] for _ in range(self.cell_height)]
        
        return grid
   

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for y in range(self.cell_height):
            for x in range(self.cell_width):
                if self.grid[y][x] == 0:
                    COLOR = [255, 255, 255]
                else:
                    COLOR = [0, 255, 0]
                pygame.draw.rect(self.screen,
                                 COLOR,
                                 (
                                     x * self.cell_size + 1,
                                     y * self.cell_size + 1,
                                     self.cell_size - 1,
                                     self.cell_size - 1
                                 )
                                 )
            pass

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.
        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.
        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.
        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        
        x, y = cell
        neighbour = []
        for row in [-1, 0, 1]:
            for col in [-1, 0, 1]:
                if(
                        (row, col) != (0, 0) and
                        0 <= x + row < self.cell_height and
                        0 <= y + col < self.cell_width
                   ):
                    neighbour.append(self.grid[x + row][y + col])

        return neighbour

    def get_next_generation(self) -> grid:
        """
        Получить следующее поколение клеток.
        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        
        self.next_generation = self.create_grid(randomize=False)
        for x in range(self.cell_height):
            for y in range(self.cell_width):
                yep_neighbour = self.get_neighbours((x, y)).count(1)
                if self.grid[x][y] == 1 and yep_neighbour in [2, 3]:
                    self.next_generation[x][y] = 1
                elif self.grid[x][y] == 0 and yep_neighbour == 3:
                    self.next_generation[x][y] = 1
                else:
                    self.next_generation[x][y] = 0
                    
        return self.next_generation

if __name__ == '__main__':
    game = GameOfLife(640, 480, 20)
    game.run()
