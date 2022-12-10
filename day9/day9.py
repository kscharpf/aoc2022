import argparse
from typing import List, Set, Tuple


class Move:
    def __init__(self, move_str: str) -> None:
        fields = move_str.split(" ")
        self.dir = fields[0]
        self.val = int(fields[1])

    def __repr__(self) -> str:
        return "MOVE " + self.dir + " " + str(self.val)


def move_right(pos: Tuple[int, int], val: int) -> Tuple[int, int]:
    return pos[0], pos[1] + val


def move_left(pos: Tuple[int, int], val: int) -> Tuple[int, int]:
    return pos[0], pos[1] - val


def move_up(pos: Tuple[int, int], val: int) -> Tuple[int, int]:
    return pos[0] - val, pos[1]


def move_down(pos: Tuple[int, int], val: int) -> Tuple[int, int]:
    return pos[0] + val, pos[1]


def move_diag_ur(pos: Tuple[int, int], val: int) -> Tuple[int, int]:
    return pos[0] - val, pos[1] + val


def move_diag_ul(pos: Tuple[int, int], val: int) -> Tuple[int, int]:
    return pos[0] - val, pos[1] - val


def move_diag_dl(pos: Tuple[int, int], val: int) -> Tuple[int, int]:
    return pos[0] + val, pos[1] - val


def move_diag_dr(pos: Tuple[int, int], val: int) -> Tuple[int, int]:
    return pos[0] + val, pos[1] + val


MOVE_FUNCS = {"R": move_right, "L": move_left, "U": move_up, "D": move_down}


def dist_delta(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> Tuple[int, int]:
    return pos1[0] - pos2[0], pos1[1] - pos2[1]


def process_move(
    move: Move,
    head_pos: Tuple[int, int],
    tail_pos: Tuple[int, int],
    visited: Set[Tuple[int, int]],
) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    new_head_pos = head_pos
    new_tail_pos = tail_pos
    visited.add(new_tail_pos)
    print(f"Process move {move} current head {head_pos} tail {tail_pos}")
    for _i in range(move.val):
        # not sure if it is necessary to move 1 by 1 but starting there
        new_head_pos = MOVE_FUNCS[move.dir](new_head_pos, 1)
        delta = dist_delta(new_head_pos, new_tail_pos)
        if abs(delta[0]) <= 1 and abs(delta[1]) <= 1:
            # print(f"Head / Tail {new_head_pos} / {new_tail_pos} tail doesn't move")
            continue
        if delta[0] > 1 and abs(delta[1]) == 0:
            new_tail_pos = move_down(new_tail_pos, 1)
        elif delta[0] < -1 and abs(delta[1]) == 0:
            new_tail_pos = move_up(new_tail_pos, 1)
        elif delta[0] == 0 and delta[1] > 1:
            new_tail_pos = move_right(new_tail_pos, 1)
        elif delta[0] == 0 and delta[1] < -1:
            new_tail_pos = move_left(new_tail_pos, 1)
        else:
            if delta[0] >= 1 and delta[1] >= 1:
                new_tail_pos = move_diag_dr(new_tail_pos, 1)
            elif delta[0] >= 1 and delta[1] <= -1:
                new_tail_pos = move_diag_dl(new_tail_pos, 1)
            elif delta[0] <= -1 and delta[1] >= 1:
                new_tail_pos = move_diag_ur(new_tail_pos, 1)
            else:
                new_tail_pos = move_diag_ul(new_tail_pos, 1)
        visited.add(new_tail_pos)
        # print(f"Current Pos {new_head_pos} {new_tail_pos}")
    return new_head_pos, new_tail_pos


def main(fname: str) -> None:
    with open(fname, "r", encoding="utf-8") as infile:
        lines = [line.rstrip() for line in infile.readlines()]
        moves: List[Move] = []
        for line in lines:
            moves.append(Move(line))
        visited: Set[Tuple[int, int]] = set()
        head_pos, tail_pos = (100, 100), (100, 100)

        for move in moves:
            head_pos, tail_pos = process_move(move, head_pos, tail_pos, visited)
        print(f"Num cells visited: {len(visited)}")
        print(f"Cells visited: {visited}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    main(args.filename)
