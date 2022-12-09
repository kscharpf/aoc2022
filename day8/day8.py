import argparse as ap
from typing import List, Tuple, Dict


def get_visible_positions(
    lines: List[str], visible: Dict[Tuple[int, int], bool]
) -> None:
    for row, line in enumerate(lines):
        highest_so_far = ord("0") - 1
        for col, c in enumerate(line):
            if ord(c) > highest_so_far:
                visible[(row, col)] = True
                highest_so_far = ord(c)

        highest_so_far = ord("0") - 1
        for col in range(len(line) - 1, -1, -1):
            if ord(line[col]) > highest_so_far:
                visible[(row, col)] = True
                highest_so_far = ord(line[col])
    for col in range(len(lines[0])):
        highest_so_far = ord("0") - 1
        for row in range(len(lines)):
            if ord(lines[row][col]) > highest_so_far:
                visible[(row, col)] = True
                highest_so_far = ord(lines[row][col])
        highest_so_far = ord("0") - 1
        for row in range(len(lines) - 1, -1, -1):
            if ord(lines[row][col]) > highest_so_far:
                visible[(row, col)] = True
                highest_so_far = ord(lines[row][col])


def get_visible_positions_from_tree(
    lines: List[str], row: int, col: int
) -> Tuple[int, int, int, int]:
    r = row - 1
    src_height = lines[row][col]
    num_up = 1
    while r >= 0 and lines[r][col] < src_height:
        num_up += 1
        r -= 1
    if r < 0:
        num_up -= 1
    r = row + 1
    num_down = 1
    while r < len(lines) and lines[r][col] < src_height:
        num_down += 1
        r += 1
    if r == len(lines):
        num_down -= 1

    c = col - 1
    num_left = 1
    while c >= 0 and lines[row][c] < src_height:
        num_left += 1
        c -= 1
    if c < 0:
        num_left -= 1
    num_right = 1
    c = col + 1
    while c < len(lines[row]) and lines[row][c] < src_height:
        num_right += 1
        c += 1
    if c == len(lines[row]):
        num_right -= 1
    return (num_up, num_down, num_left, num_right)


def main(fname: str) -> None:
    with open(fname, "r", encoding="utf-8") as infile:
        lines = [line.rstrip("\n") for line in infile.readlines()]
        visible_positions: Dict[Tuple[int, int], bool] = {}
        get_visible_positions(lines, visible_positions)
        print(f"Num Visible Trees: {len(visible_positions.keys())}")
        print(sorted(list(visible_positions.keys())))

        best_value = 0
        best_position = None
        for i in range(len(lines)):
            for j in range(len(lines[0])):
                visible = get_visible_positions_from_tree(lines, i, j)
                up, down, left, right = visible
                # print(f"Position {i,j}: {visible}")
                if up * down * left * right > best_value:
                    best_value = up * down * left * right
                    best_position = (i, j)
        print(f"Best Position is {best_position} with value {best_value}")


if __name__ == "__main__":
    parser = ap.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    main(args.filename)
