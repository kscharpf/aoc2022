import argparse
from typing import List, Tuple, NamedTuple, Optional
from dataclasses import dataclass, field


class RockEndpoint(NamedTuple):
    row: int
    col: int


class RockLine(NamedTuple):
    start: RockEndpoint
    end: RockEndpoint


def get_rock_point(rock_point_str: str) -> RockEndpoint:
    col, row = [int(x) for x in rock_point_str.split(",")]
    return RockEndpoint(row, col)


def build_rock_line(start: RockEndpoint, end: RockEndpoint) -> RockLine:
    if start.col > end.col:
        return RockLine(end, start)
    if start.row > end.row:
        return RockLine(end, start)
    return RockLine(start, end)


def is_horizontal(line: RockLine) -> bool:
    if line.start.row == line.end.row:
        return True
    return False


@dataclass
class CaveMap:
    min_col: int
    max_col: int
    min_row: int
    max_row: int
    horizontal_lines: List[RockLine] = field(default_factory=list)
    vertical_lines: List[RockLine] = field(default_factory=list)
    display: List[List[str]] = field(default_factory=list)

    def __init__(self, row: int, col: int):
        self.min_row = self.max_row = row
        self.min_col = self.max_col = col
        self.horizontal_lines = []
        self.vertical_lines = []
        self.display = []

    def init_map(self) -> None:
        for _i in range(self.min_row, self.max_row + 2):
            self.display.append([])
            for _j in range(self.min_col, self.max_col + 1):
                self.display[-1].append(".")
        for row in range(self.min_row, self.max_row + 2):
            for col in range(self.min_col, self.max_col + 1):
                if self.is_rock(row, col):
                    self.display[row - self.min_row][col - self.min_col] = "#"

    def is_horizontal_rock(self, row: int, col: int) -> bool:
        for rock_line in self.horizontal_lines:
            if rock_line.start.row != row:
                continue

            if rock_line.start.col <= col <= rock_line.end.col:
                return True
        return False

    def is_vertical_rock(self, row: int, col: int) -> bool:
        for rock_line in self.vertical_lines:
            if rock_line.start.col != col:
                continue

            if rock_line.start.row <= row <= rock_line.end.row:
                return True
        return False

    def is_rock(self, row: int, col: int) -> bool:
        return self.is_horizontal_rock(row, col) or self.is_vertical_rock(row, col)

    def draw(self) -> str:
        print(self.display)

        display_list: List[str] = []
        for record in self.display:
            display_list.append("".join(s for s in record))
        return "\n".join(s for s in display_list)

    def add_rock_line(self, rock_line: RockLine) -> None:
        self.min_col, self.max_col = min(self.min_col, rock_line.start.col), max(
            self.max_col, rock_line.start.col
        )
        self.min_row, self.max_row = min(self.min_row, rock_line.start.row), max(
            self.max_row, rock_line.start.row
        )
        self.min_col, self.max_col = min(self.min_col, rock_line.end.col), max(
            self.max_col, rock_line.end.col
        )
        self.min_row, self.max_row = min(self.min_row, rock_line.end.row), max(
            self.max_row, rock_line.end.row
        )

        if is_horizontal(rock_line):
            self.horizontal_lines.append(rock_line)
            return

        print(self)
        self.vertical_lines.append(rock_line)

    def add_rock_structure(self, line: str) -> None:
        rock_points = line.split(" -> ")

        start_point: Optional[RockEndpoint] = None
        for i, rock_point_str in enumerate(rock_points):
            rock_point = get_rock_point(rock_point_str)
            if i == 0:
                start_point = rock_point
                continue
            assert start_point is not None
            self.add_rock_line(build_rock_line(start_point, rock_point))
            start_point = rock_point

    def is_air(self, row: int, col: int) -> bool:
        row_offset = row - self.min_row
        col_offset = col - self.min_col

        if row_offset >= len(self.display):
            self.display.append(["."] * (self.max_col - self.min_col + 1))

        if col_offset < 0:
            for row in range(self.min_row, self.max_row + 2):
                self.display[row].insert(0, ".")
            self.min_col -= 1
            return True

        if col_offset >= len(self.display[row_offset]):
            for row in range(self.min_row, self.max_row + 2):
                self.display[row].append(".")
            self.max_col += 1
            return True

        return self.display[row_offset][col_offset] == "."

    def is_floor(self, row: int, col: int) -> bool:
        return row == self.max_row + 2

    def set_sand(self, row: int, col: int) -> None:
        row_offset = row - self.min_row
        col_offset = col - self.min_col

        assert col_offset >= 0
        assert row_offset >= 0

        if row_offset >= len(self.display):
            print(f"EXPAND ROW")
            self.display.append(["."] * (self.max_col - self.min_col + 1))
        if col_offset >= len(self.display[row_offset]):
            print(f"EXPAND COL offset {col_offset} len {len(self.display[row_offset])}")
            for row in range(self.min_row, self.max_row + 1):
                self.display[row].append(".")

        self.display[row_offset][col_offset] = "o"

    def fall(self, row: int, col: int) -> bool:
        self.min_col, self.max_col = min(self.min_col, col), max(self.max_col, col)

        if row == self.max_row + 1:
            self.set_sand(row, col)
            return False

        if self.is_air(row + 1, col):
            return self.fall(row + 1, col)
        elif self.is_air(row + 1, col - 1):
            return self.fall(row + 1, col - 1)
        elif self.is_air(row + 1, col + 1):
            return self.fall(row + 1, col + 1)
        else:
            if row == 0 and col == 500:
                return True
            self.set_sand(row, col)
        return False


def build_map(lines: List[str]) -> CaveMap:
    """
    Convert the input text into a map of the cave

    Params:
        lines: list of strings defining routes

    Returns:
        Representation of the cave
    """
    cave_map = CaveMap(0, 500)
    for line in lines:
        cave_map.add_rock_structure(line)

    cave_map.init_map()
    print(cave_map.draw())
    return cave_map


def drop_sand(cave_map: CaveMap) -> bool:
    """
    Drop a grain of sand from the 500, 0 position in
    the cave. Update the map to reflect the resting
    coordinates of this sand. If the sand does not
    come to rest, return False.

    Params:
        cave_map: abstract representation of the cave

    Returns:
        True, if the sand came to rest. False otherwise
    """
    return cave_map.fall(0, 500)


def main(filename: str) -> None:
    with open(filename, "r", encoding="utf-8") as infile:
        lines = [line.rstrip("\n") for line in infile.readlines()]
        cave_map = build_map(lines)

        sand_drops = 1
        while True:
            if drop_sand(cave_map):
                break
            sand_drops += 1

        print(cave_map.draw())
        print(f"Number of drops: {sand_drops}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    main(args.filename)
