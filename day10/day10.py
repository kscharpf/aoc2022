"""
Python solution for Advent of Code 2022 Day 10
"""
import argparse as ap
from typing import List, Union


class NoopInstruction:
    def __init__(self) -> None:
        self.cycles_remaining = 1
        self.value = 0

    def __repr__(self) -> str:
        return f"NOOP - Remaining {self.cycles_remaining}"


class AddxInstruction:
    def __init__(self, value: int) -> None:
        self.cycles_remaining = 2
        self.value = value

    def __repr__(self) -> None:
        return f"ADDX({self.value}) Remaining {self.cycles_remaining}"


def build_instruction(insstr: str) -> Union[NoopInstruction, AddxInstruction]:
    fields = insstr.split(" ")

    if fields[0] == "addx":
        return AddxInstruction(int(fields[1]))

    return NoopInstruction()


class StateMachine:
    def __init__(self, program: List[Union[NoopInstruction, AddxInstruction]]) -> None:
        self.program = program

    def run(self, num_cycles: int, cycles_of_interest: List[int]) -> int:
        active_instruction = self.program[0]
        self.program = self.program[1:]
        total = 0
        sprite_x = 1
        for cycle in range(1, num_cycles):
            active_instruction.cycles_remaining -= 1
            # print(f"Cycle {cycle} Begin Active Instruction {active_instruction} xval {sprite_x}")
            if cycle in cycles_of_interest:
                total += cycle * sprite_x
            if active_instruction.cycles_remaining == 0:
                sprite_x += active_instruction.value

                if not self.program:
                    print(f"Program Complete")
                    return total
                active_instruction = self.program[0]
                self.program = self.program[1:]
            # print(f"Cycle {cycle} AFTER xval {sprite_x} ")
        return total


def main(fname: str, num_cycles: int) -> None:
    with open(fname, "r", encoding="utf-8") as infile:
        lines = [line.rstrip() for line in infile.readlines()]
        program = [build_instruction(line) for line in lines]
        machine = StateMachine(program)
        result = machine.run(num_cycles, [20, 60, 100, 140, 180, 220])
        print(f"Part1 Solution: {result}")


if __name__ == "__main__":
    parser = ap.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("--num-cycles", default=20, type=int)
    args = parser.parse_args()
    main(args.filename, args.num_cycles)
