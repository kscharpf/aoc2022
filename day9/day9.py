"""
Python solution for Advent of Code 2022 Day 9
"""
import argparse
from typing import List, Set, Tuple, NamedTuple


class Move(NamedTuple):
    """
    Object abstraction of a Move
    """

    dir: str
    val: int


def make_move(move_str: str) -> Move:
    """
    Decompose the move string into a Move object
    Params:
        move_str: string of the form <DIR> <MAGNITUDE>
    Returns:
        Move object
    """
    fields = move_str.split(" ")
    direction = fields[0]
    val = int(fields[1])
    return Move(direction, val)


def clamp(val: int, low: int, high: int) -> int:
    """
    Restrict a value to the range of low<=val<=high
    Params:
        val: magnitude
        low: minimum value
        high: maximum value
    Return:
        clamped magnitude
    """
    return max(low, min(val, high))


def do_move(pos: Tuple[int, int], delta: Tuple[int, int]) -> Tuple[int, int]:
    """
    Move from the position in accordance with the change magnitude in both
    the row and column dimensions. Moves are clamped to an amplitude of 1.
    Params:
        pos: Row and Column of the current position
        delta: Row delta and column delta to apply from the current position
    Returns:
        Row and column tuple representing the new position
    """
    return pos[0] + clamp(delta[0], -1, 1), pos[1] + clamp(delta[1], -1, 1)


MOVE_MAP = {"R": (0, 1), "L": (0, -1), "U": (-1, 0), "D": (1, 0)}


def dist_delta(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> Tuple[int, int]:
    """
    Calculate the delta between the two positions
    Params:
        pos1: row and column tuple
        pos2: row and column tuple
    Returns:
        row delta, column delta
    """
    return pos1[0] - pos2[0], pos1[1] - pos2[1]


def process_move(
    move: Move,
    positions: List[Tuple[int, int]],
    visited: List[Set[Tuple[int, int]]],
) -> List[Tuple[int, int]]:
    """
    process_move takes a move object and processes each knot in order.
    Params:
        move: Move object - direction and magnitude
        positions: Position of each knot on the rope
        visited: All positions visited for each of the knots
    Returns:
        List[Tuple[int, int]]: The new positions of each knot in the rope
    """
    new_positions: List[Tuple[int, int]] = []
    for i, pos in enumerate(positions):
        visited[i].add(pos)
        new_positions.append(pos)

    for _i in range(move.val):
        for j in range(len(positions)):
            visited[j].add(new_positions[j])
            if j == 0:
                new_positions[0] = do_move(new_positions[0], MOVE_MAP[move.dir])
            else:
                delta = dist_delta(new_positions[j - 1], new_positions[j])
                if abs(delta[0]) <= 1 and abs(delta[1]) <= 1:
                    continue

                new_positions[j] = do_move(new_positions[j], delta)
    return new_positions


def main(fname: str, num_knots: int) -> None:
    """
    Process parts 1 and 2
    Params:
        fname: str - filename
        num_knots: int - number of knots in the rope - 2 for p1, 10 for p2
    Returns: None
    """
    with open(fname, "r", encoding="utf-8") as infile:
        lines = [line.rstrip() for line in infile.readlines()]
        moves: List[Move] = []
        for line in lines:
            moves.append(make_move(line))
        visited: List[Set[Tuple[int, int]]] = []

        positions: List[Tuple[int, int]] = []
        for _i in range(num_knots):
            visited.append(set())
            positions.append((0, 0))

        for move in moves:
            positions = process_move(move, positions, visited)

        for i in range(num_knots):
            print(f"Knot {i} Num cells visited: {len(visited[i])}")
        # print(f"Cells visited: {visited}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("--num-knots", default=2, type=int)
    args = parser.parse_args()
    main(args.filename, args.num_knots)
