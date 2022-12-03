import sys
import argparse

ROCK = 1
PAPER = 2
SCIZZORS = 3

LOSE = 0
DRAW = 3
WIN = 6

MOVES = {"A": ROCK, "B": PAPER, "C": SCIZZORS, "X": ROCK, "Y": PAPER, "Z": SCIZZORS}
MOVES2 = {"A": ROCK, "B": PAPER, "C": SCIZZORS}
RESULT = {"X": LOSE, "Y": DRAW, "Z": WIN}
ADVANTAGE = {ROCK: SCIZZORS, SCIZZORS: PAPER, PAPER: ROCK}
DISADVANTAGE = {SCIZZORS: ROCK, PAPER: SCIZZORS, ROCK: PAPER}


def winner(oppo_move, my_move):
    if oppo_move == my_move:
        return 3
    elif oppo_move == ROCK and my_move == PAPER:
        return 6
    elif oppo_move == ROCK and my_move == SCIZZORS:
        return 0
    elif oppo_move == PAPER and my_move == ROCK:
        return 0
    elif oppo_move == PAPER and my_move == SCIZZORS:
        return 6
    elif oppo_move == SCIZZORS and my_move == ROCK:
        return 6
    else:
        return 0


def part1_main(fname):
    with open(fname, "r") as infile:
        lines = infile.readlines()
        total_points = 0
        for line in lines:
            moves = [MOVES[move.rstrip()] for move in line.split(" ")]
            oppo_move, my_move = moves[0], moves[1]
            points = winner(oppo_move, my_move) + my_move
            total_points += points

        print(f"Total: {total_points}")


def part2_main(fname):
    with open(fname, "r") as infile:
        lines = infile.readlines()
        total_points = 0
        for line in lines:
            oppo_move_str, my_result_str = line.rstrip("\n").split(" ")
            oppo_move = MOVES[oppo_move_str]
            if RESULT[my_result_str] == DRAW:
                total_points += oppo_move + DRAW
            elif RESULT[my_result_str] == WIN:
                total_points += DISADVANTAGE[oppo_move] + WIN
            else:
                total_points += ADVANTAGE[oppo_move] + LOSE

        print(f"Total: {total_points}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--part1", action="store_true")
    parser.add_argument("filename")

    args = parser.parse_args()
    if args.part1:
        part1_main(args.filename)
    else:
        part2_main(args.filename)
