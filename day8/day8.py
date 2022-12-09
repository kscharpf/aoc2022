"""
Advent of Code 2022 Day 8 Solution
"""
import argparse as ap
from functools import reduce
from typing import List, Tuple, Set


def get_visible_positions(lines: List[str], visible: Set[Tuple[int, int]]) -> None:
    """
    Find all positions visible from the edges
    Params:
        lines: list of strings defining tree heights
        visible:
    Returns: None
    """
    for row, line in enumerate(lines):
        highest_so_far = ord("0") - 1
        for col, char in enumerate(line):
            if ord(char) > highest_so_far:
                visible.add((row, col))
                highest_so_far = ord(char)

        highest_so_far = ord("0") - 1
        for col in range(len(line) - 1, -1, -1):
            if ord(line[col]) > highest_so_far:
                visible.add((row, col))
                highest_so_far = ord(line[col])
    for col in range(len(lines[0])):
        highest_so_far = ord("0") - 1
        for row, line in enumerate(lines):
            if ord(line[col]) > highest_so_far:
                visible.add((row, col))
                highest_so_far = ord(line[col])
        highest_so_far = ord("0") - 1
        for row in range(len(lines) - 1, -1, -1):
            if ord(lines[row][col]) > highest_so_far:
                visible.add((row, col))
                highest_so_far = ord(lines[row][col])


def get_visible_positions_from_tree(
    lines: List[str], src_row: int, src_col: int
) -> Tuple[int, int, int, int]:
    """
    Find all trees visible in each direction from a given
    source tree.
    Params:
        list: list of strings defining the forest
        src_row: row number of the source tree
        src_col: col number of the source tree
    Returns:
        Tuple: number of visible trees in each direction,
        up, down, left, right
    """
    row = src_row - 1
    src_height = lines[src_row][src_col]
    num_up = 1
    while row >= 0 and lines[row][src_col] < src_height:
        num_up += 1
        row -= 1
    if row < 0:
        num_up -= 1
    row = src_row + 1
    num_down = 1
    while row < len(lines) and lines[row][src_col] < src_height:
        num_down += 1
        row += 1
    if row == len(lines):
        num_down -= 1

    col = src_col - 1
    num_left = 1
    while col >= 0 and lines[src_row][col] < src_height:
        num_left += 1
        col -= 1
    if col < 0:
        num_left -= 1
    num_right = 1
    col = src_col + 1
    while col < len(lines[src_row]) and lines[src_row][col] < src_height:
        num_right += 1
        col += 1
    if col == len(lines[src_row]):
        num_right -= 1
    return (num_up, num_down, num_left, num_right)


def main(fname: str) -> None:
    """
    Main function for the AOC 2022 solution
    Params:
        fname: filename of input text
    Returns: None
    """
    with open(fname, "r", encoding="utf-8") as infile:
        lines = [line.rstrip("\n") for line in infile.readlines()]
        visible_positions: Set[Tuple[int, int]] = set()
        get_visible_positions(lines, visible_positions)
        print(f"Num Visible Trees: {len(visible_positions)}")
        print(sorted(visible_positions))

        all_beauty = [
            reduce(lambda x, y: x * y, get_visible_positions_from_tree(lines, i, j))
            for j in range(len(lines[0]))
            for i in range(len(lines))
        ]
        print(f"Best Value {max(all_beauty)}")


if __name__ == "__main__":
    parser = ap.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    main(args.filename)
