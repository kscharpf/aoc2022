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
        self.crt: List[str] = []

    def draw_pixel(self, cycle: int, sprite_x: int) -> None:
        row_num = (cycle - 1) // 40
        if row_num >= len(self.crt):
            self.crt.append("")
        draw_col = (cycle - 1) % 40
        if abs(sprite_x - draw_col) <= 1:
            self.crt[-1] += "#"
        else:
            self.crt[-1] += "."

    def display(self) -> str:
        return "\n".join(self.crt)

    def run(self, cycles_of_interest: List[int]) -> int:
        active_instruction = self.program[0]
        self.program = self.program[1:]
        total = 0
        sprite_x = 1
        cycle = 1
        done = False
        while not done:
            self.draw_pixel(cycle, sprite_x)
            active_instruction.cycles_remaining -= 1
            if cycle in cycles_of_interest:
                total += cycle * sprite_x
            if active_instruction.cycles_remaining == 0:
                sprite_x += active_instruction.value

                if not self.program:
                    break

                active_instruction = self.program[0]
                self.program = self.program[1:]
            cycle += 1
        return total


def main(fname: str) -> None:
    with open(fname, "r", encoding="utf-8") as infile:
        lines = [line.rstrip() for line in infile.readlines()]
        program = [build_instruction(line) for line in lines]
        machine = StateMachine(program)
        result = machine.run([20, 60, 100, 140, 180, 220])
        print(f"Part1 Solution: {result}")
        print(machine.display())


if __name__ == "__main__":
    parser = ap.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    main(args.filename)
