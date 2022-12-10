"""
Python solution for Advent of Code 2022 Day 10
"""
import argparse as ap
from typing import List, Union
from dataclasses import dataclass

@dataclass
class NoopInstruction:
    """
    No-op abstraction
    """
    cycles_remaining: int
    value: int

@dataclass
class AddxInstruction:
    """
    addx instruction abstraction
    """
    cycles_remaining: int
    value: int

Instruction = Union[NoopInstruction, AddxInstruction]


def build_instruction(insstr: str) -> Instruction:
    """
    Create instruction object from line string
    Params:
        insstr: string of form <instruction> Optional[value]
    Returns:
        Instruction object
    """
    fields = insstr.split(" ")

    if fields[0] == "addx":
        return AddxInstruction(2, int(fields[1]))

    return NoopInstruction(1, 0)


class StateMachine:
    """
    CPU abstraction
    """

    def __init__(self, program: List[Instruction]) -> None:
        """
        Constructor for the state machine
        Params:
            program: list of instructions
        Return: None
        """
        self.program = program
        self.crt: List[str] = []

    def draw_pixel(self, cycle: int, sprite_x: int) -> None:
        """
        Draw the pixel on the CRT
        Params:
            cycle: int - clock cycle
            sprite_x: int - current sprite position
        Return: None
        """
        row_num = (cycle - 1) // 40
        if row_num >= len(self.crt):
            self.crt.append("")
        draw_col = (cycle - 1) % 40
        if abs(sprite_x - draw_col) <= 1:
            self.crt[-1] += "#"
        else:
            self.crt[-1] += "."

    def display(self) -> str:
        """
        Return the CRT as a single string
        Params: None
        Return: None
        """
        return "\n".join(self.crt)

    def run(self, cycles_of_interest: List[int]) -> int:
        """
        Execute the state machine
        Params:
            cycles_of_interest: The cycles to track for the part1 solution
        Return:
            Part1 total value
        """
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
    """
    Execute the day10 solution for parts1 and 2
    Params:
        fname: input filename
    Return: None
    """
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
