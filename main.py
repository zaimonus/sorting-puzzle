from dataclasses import dataclass
import random


@dataclass
class Grid:
    width: int
    height: int
    pool: list[int]
    default: int = 0
    _grid: list[list[int]] = None

    @property
    def initialized(self) -> bool:
        return self._grid is not None
    
    @property
    def columns(self) -> list[list[int]]:
        return [list(c) for c in self._grid]

    @property
    def solved(self) -> bool:
        return all((
            all((item == column[0] for item in column)) for column in self.columns
        ))

    def __create_grid(self) -> None:
        self._grid = [list() for _ in range(self.width)]

    def __fill_grid(self) -> None:
        values = list(self.pool)
        free_columns = list(range(self.width))
        while len(values) > 0 and len(free_columns) > 0:
            column = random.choice(free_columns)
            self._grid[column].append(values.pop())
            if len(self._grid[column]) >= self.height:
                free_columns.remove(column)

    def init(self) -> None:
        self.__create_grid()
        self.__fill_grid()

    def reset(self) -> None:
        self._grid = None
    
    def switch(self, src_column: int, dest_column: int) -> None:
        if src_column < 0 or src_column >= self.width:
            raise IndexError(f"This column does not exist: {src_column + 1}")
        if dest_column < 0 or dest_column >= self.width:
            raise IndexError(f"This column does not exist: {dest_column + 1}")
        if len(self.columns[src_column]) == 0:
            raise IndexError(f"This column is empty: {src_column + 1}")
        if len(self.columns[dest_column]) == self.height:
            raise IndexError(f"This column is full: {dest_column + 1}")
        top = self._grid[src_column].pop()
        self._grid[dest_column].append(top)

    def __str__(self) -> str:
        grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        
        for x, column in enumerate(self._grid):
            for y, item in enumerate(column):
                grid[self.height - y - 1][x] = item
        
        str_item_grid = [map(str, row) for row in grid]
        str_rows = [" | ".join(row) for row in str_item_grid]
        return "\n".join(str_rows)

class Pool:

    @staticmethod
    def from_tuples(items: list[tuple[int, int]]) -> list[int]:
        return [k for k, v in items() for _ in range(v)]

    @staticmethod
    def from_dict(items: dict[int, int]) -> list[int]:
        return [k for k, v in items.items() for _ in range(v)]

    @staticmethod
    def balanced(items: list[int], total: int) -> list[int]:
        each = total // len(items)
        return [item for _ in range(each) for item in items]

def main():
    p = Pool.balanced([1, 2, 3, 4, 5], 5 * 5 - 1)
    g = Grid(width=5, height=5, pool=p)
    g.init()
    print(g)

    while not g.solved:
        src_col = int(input("// from >"))
        dest_col = int(input("//  to  >"))
        print(f"switch from col {src_col} to {dest_col}")
        try:
            g.switch(src_col - 1, dest_col - 1)
            print(g)
        except IndexError as e:
            print(e)
        
    print("Hurray!! You#ve made it!!")

main()
