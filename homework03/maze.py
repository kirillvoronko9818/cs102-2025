from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """

    x, y = coord
    new_grid = deepcopy(grid)

    directions = []

    if x > 1 and new_grid[x - 1][y] == "■":
        directions.append("up")
    if y < len(new_grid[0]) - 2 and new_grid[x][y + 1] == "■":
        directions.append("right")
    if not directions:
        return new_grid

    direction = choice(directions)
    if direction == "up":
        new_grid[x - 1][y] = " "
    elif direction == "right":
        new_grid[x][y + 1] = " "

    return new_grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки
    for x, y in empty_cells:
        direction = choice(["up", "right"])
        may_go_up = x > 1
        may_go_right = y < cols - 2

        if direction == "up":
            if may_go_up:
                grid[x - 1][y] = " "
            elif may_go_right:
                grid[x][y + 1] = " "
        elif direction == "right":
            if may_go_right:
                grid[x][y + 1] = " "
            elif may_go_up:
                grid[x - 1][y] = " "

    # генерация входа и выхода
    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """

    result = []

    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if grid[x][y] == "X":
                result.append((x, y))
                if len(result) == 2:
                    return result
    return result


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """

    rows, cols = len(grid), len(grid[0])
    new_grid = deepcopy(grid)

    for x in range(rows):
        for y in range(cols):
            if new_grid[x][y] == k:
                closest = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
                for cx, cy in closest:
                    if 0 <= cx < rows and 0 <= cy < cols:
                        if new_grid[cx][cy] == 0 or new_grid[cx][cy] == " ":
                            new_grid[cx][cy] = k + 1
    return new_grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """
    numbers_rows = len(grid)
    numbers_cols = len(grid[0])
    x, y = exit_coord
    k = int(grid[x][y])
    path = [(x, y)]

    while k > 1:
        k -= 1
        neighbours = [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]
        for coord_x, coord_y in neighbours:
            if 0 <= coord_x < numbers_rows and 0 <= coord_y < numbers_cols:
                if grid[coord_x][coord_y] == k:
                    path.append((coord_x, coord_y))
                    x, y = coord_x, coord_y
                    break
        else:
            break
    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """

    if coord[0] == len(grid) - 1 and coord[1] == len(grid[0]) - 1:
        return True
    elif coord[0] == 0 and coord[1] == 0:
        return True
    elif coord[0] == 0 and coord[1] == len(grid[0]) - 1:
        return True
    elif coord[0] == len(grid) - 1 and coord[1] == 0:
        return True
    if coord[0] == len(grid) - 1:
        if grid[coord[0] - 1][coord[1]] != " ":
            return True
    elif coord[0] == 0:
        if grid[coord[0] + 1][coord[1]] != " ":
            return True
    elif coord[1] == len(grid[0]) - 1:
        if grid[coord[0]][coord[1] - 1] != " ":
            return True
    elif coord[1] == 0:
        if grid[coord[0]][coord[1] + 1] != " ":
            return True
    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """

    :param grid:
    :return:
    """

    exits = get_exits(grid)
    if len(exits) != 2:
        return grid, None
    for possible_exit in exits:
        if encircled_exit(grid, possible_exit):
            return grid, None

    start_coord, end_coord = exits
    next_grid = deepcopy(grid)
    for row_idx, row in enumerate(next_grid):
        for col_idx, cell in enumerate(row):
            if cell == " ":
                next_grid[row_idx][col_idx] = 0
    next_grid[start_coord[0]][start_coord[1]] = 1
    next_grid[end_coord[0]][end_coord[1]] = 0

    k = 1
    while next_grid[end_coord[0]][end_coord[1]] == 0:
        prev_next_grid = deepcopy(next_grid)
        next_grid = make_step(next_grid, k)
        if next_grid == prev_next_grid:
            return grid, None
        k += 1

    path = shortest_path(next_grid, end_coord)
    return grid, path


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
