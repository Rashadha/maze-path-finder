from enum import Enum
from typing import List, NamedTuple, Callable, Optional
import random
from search import dfs, select_path, Node, a_star


class Cell(str, Enum):
    EMPTY = "   "
    BLOCKED = " X "
    START = " S "
    GOAL = " G "
    PATH = " * "


class MazeLocation(NamedTuple):
    row: int
    column: int


class Maze:
    def __init__(self, rows: int = 6, columns: int = 6,
                 spar_senses: float = 0.2,
                 start: MazeLocation = MazeLocation(random.randint(0, 5), random.randint(0, 1)),
                 goal: MazeLocation = MazeLocation(random.randint(0, 5), random.randint(4, 5))) -> None:
        self._rows: int = rows
        self._columns: int = columns
        self.start: MazeLocation = start
        self.goal: MazeLocation = goal

        # Filling the maze with empty cells
        self._grid: List[List[Cell]] = [[Cell.EMPTY for c in range(columns)]
                                        for r in range(rows)]

        # blocking the cells
        self._block_cells(rows, columns, spar_senses)

        self._grid[start.row][start.column] = Cell.START
        self._grid[goal.row][goal.column] = Cell.GOAL

    def _block_cells(self, rows: int, columns: int, spar_senses: float):
        for row in range(rows):
            for column in range(columns):
                if random.uniform(0, 1.0) < spar_senses:
                    self._grid[row][column] = Cell.BLOCKED

    # printing the maze
    def __str__(self) -> str:
        out: str = ""
        for row in self._grid:
            out += "".join([c.value for c in row]) + "\n"
        return out

    def test_goal(self, ml: MazeLocation) -> bool:
        return ml == self.goal

    def move(self, ml: MazeLocation) -> List[MazeLocation]:
        locations: List[MazeLocation] = []
        # move left
        if ml.column - 1 >= 0 and self._grid[ml.row][ml.column - 1] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.column - 1))
        # move up
        if ml.row - 1 >= 0 and self._grid[ml.row - 1][ml.column] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row - 1, ml.column))
        # move down
        if ml.row + 1 < self._rows and self._grid[ml.row + 1][ml.column] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row + 1, ml.column))
        # move right
        if ml.column + 1 < self._columns and self._grid[ml.row][ml.column] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.column + 1))
        return locations

    def mark_path(self, path: List[MazeLocation]):
        for ml in path:
            self._grid[ml.row][ml.column] = Cell.PATH
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL

    def clear_path(self, path: List[MazeLocation]):
        for ml in path:
            self._grid[ml.row][ml.column] = Cell.EMPTY
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL


def chebyshev_distance(goal: MazeLocation):
    def distance(ml: MazeLocation):
        x_distance: int = abs(ml.column - goal.column)
        y_distance: int = abs(ml.row - goal.row)
        return max(x_distance, y_distance)

    return distance

m: Maze = Maze()
print("DFS")
print(m)
print()
solution: Optional[Node[MazeLocation]] = dfs(m.start, m.test_goal, m.move)
if solution is None:
    print("No solution found")
else:
    path1: List[MazeLocation] = select_path(solution)
    m.mark_path(path1)
    print()
    print(m)
    print()
    m.clear_path(path1)

print("A*")
print()
print(m)
print()

distance: Callable[[MazeLocation], float] = chebyshev_distance(m.goal)
solution2: Optional[Node[MazeLocation]] = a_star(m.start, m.test_goal,
                                                     m.move, distance)
if solution2 is None:
    print("No solution found")
else:
    print()
    path2: List[MazeLocation] = select_path(solution2)
    m.mark_path(path2)
    print(m)
