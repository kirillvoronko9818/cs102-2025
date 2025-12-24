import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
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
        self.grid = self.create_grid(randomize=True)
    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_lines()
            self.draw_grid()
            self.grid = self.get_next_generation()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
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
        grid = []
        for row in range(self.cell_height):
            grid_row = []
            for col in range(self.cell_width):
                if randomize:
                    cell_value = random.randint(0, 1)
                else:
                    cell_value = 0
                grid_row.append(cell_value)
            grid.append(grid_row)
        return grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for row in range(self.cell_height):
            for col in range(self.cell_width):
                x = col * self.cell_size
                y = row * self.cell_size
                cell_rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                if self.grid[row][col] == 1:
                    color = pygame.Color("green")
                else:
                    color = pygame.Color("white")
                pygame.draw.rect(self.screen, color, cell_rect)

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
        row, col = cell
        neighbours = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                neighbour_row = row + i
                neighbour_col = col + j
                if 0 <= neighbour_row < self.cell_height and 0 <= neighbour_col < self.cell_width:
                    neighbours.append(self.grid[neighbour_row][neighbour_col])
        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        new_grid = []
        for row in range(self.cell_height):
            new_row = []
            for col in range(self.cell_width):
                current_cell = self.grid[row][col]
                neighbours = self.get_neighbours((row, col))
                alive_neighbours = sum(neighbours)
                if current_cell == 1:
                    if alive_neighbours in (2, 3):
                        new_row.append(1)
                    else:
                        new_row.append(0)
                else:
                    if alive_neighbours == 3:
                        new_row.append(1)
                    else:
                        new_row.append(0)
            new_grid.append(new_row)
        return new_grid
