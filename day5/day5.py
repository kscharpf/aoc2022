"""
Advent of Code Day5
"""
import argparse as ap
import re
from typing import List, Tuple

CRATE_MOVER_9000 = "CrateMover9000"
CRATE_MOVER_9001 = "CrateMover9001"

def parse_drawing_line(line_index: int, line: str) -> List[Tuple[str, int, int]]:
    """
    A line in the drawing looks like
    <spaces>OPEN_BRACKET CHAR CLOSE_BRACKET<spaces>OPEN_BRACKET CHAR CLOSE_BRACKET...

    The spaces determine the stack number this is. The character inside the brackets
    determines the label of the crate. Return a list of label, stack number, height
    tuples for everything found in this row.
    """
    line = line.rstrip("\n")
    i = 0
    stack_num = 1
    crates: List[Tuple[str, int, int]] = []

    while i < len(line):
        if line[i] == ' ':
            i += 4
            stack_num += 1
        elif line[i] == '[':
            crates.append((line[i+1], stack_num, line_index))
            i += 4
            stack_num += 1
    print(f"Line {line} has crates {crates}")
    return crates

def move_crates_9001(crates: List[List[str]], src: int, dest: int, num_crates: int) -> None:
    crates_to_move = crates[src - 1][-num_crates:]
    crates[src - 1] = crates[src - 1][:-num_crates]
    crates[dest - 1].extend(crates_to_move)

def move_crates_9000(crates: List[List[str]], src: int, dest: int, num_crates: int) -> None:
    for _i in range(num_crates):
        crate = crates[src-1].pop()
        crates[dest-1].append(crate)

def main(fname: str, is_crate_mover_9001: bool) -> None:
    with open(fname, "r", encoding="utf-8") as infile:
        lines = infile.readlines()
        move_lines = []
        stacks: List[List[str]] = []
        for index, line in enumerate(lines):
            new_crates = parse_drawing_line(index, line)
            if not new_crates:
                move_lines = lines[index+2:]
                break
            for crate in new_crates:
                label, stack_num, height = crate
                for i in range(len(stacks), stack_num, 1):
                    stacks.append([])
                stacks[stack_num - 1].append(label)
        for i in range(len(stacks)):
            stacks[i] = stacks[i][::-1]

        move_re = re.compile(r"move (\d+) from (\d+) to (\d+)")
        for index, line in enumerate(move_lines):
            match = move_re.findall(line.rstrip())
            if match:
                print(f"Move {match[0][0]} from {match[0][1]} to {match[0][2]}")
                num_crates_to_move = int(match[0][0])
                from_stack = int(match[0][1])
                to_stack = int(match[0][2])
                if is_crate_mover_9001:
                    move_crates_9001(stacks, from_stack, to_stack, num_crates_to_move)
                else:
                    move_crates_9000(stacks, from_stack, to_stack, num_crates_to_move)
                #for i in range(num_crates_to_move):
                    #val = stacks[from_stack-1].pop()
                    #stacks[to_stack-1].append(val)
        for index, stack in enumerate(stacks):
            print(f"Top of stack {index+1} is {stack[-1]}")
        result_str = "".join([stack[-1] for stack in stacks])
        print(f"Result: {result_str}")


if __name__ == "__main__":
    parser = ap.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("--crate-mover-9001", action="store_true")
    args = parser.parse_args()
    main(args.filename, args.crate_mover_9001)