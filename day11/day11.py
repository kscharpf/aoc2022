"""
Advent of Code 2022 Day 11 Python solution
"""
import argparse as ap
from dataclasses import dataclass
from typing import List, Tuple, Dict
import re

Expression = str


def parse_worry_operation(lines: List[str]) -> Expression:
    """
    Pull out the next worry operation
    Params: lines - remaining unparsed program lines
    Returns: None
    """
    worry_re = re.compile(r".*Operation: new = (.*)$")
    match = worry_re.findall(lines[0])
    assert match
    return Expression(match[0])


@dataclass
class TestOperation:
    """
    Class modeling the monkey's test operation
    """

    divisor: int
    throw_true_monkey: int
    throw_false_monkey: int

    def execute(self, worry: int, all_monkeys: Dict[int, "Monkey"]) -> None:
        """
        Monkey tests the item by determining if the level of worry is divisible
        by this monkey's divisor. Depending on that result, throw to the next
        appropriate monkey.
        Params:
            worry: level of worry associated with this item
            all_monkeys: Dictionary mapping monkey ids to monkey objects
        Returns: None
        """
        if worry % self.divisor == 0:
            all_monkeys[self.throw_true_monkey].item_worries.append(worry)
        else:
            all_monkeys[self.throw_false_monkey].item_worries.append(worry)


def parse_test_operation(lines: List[str]) -> TestOperation:
    """
    Convert the next three lines into a TestOperation object
    Params: lines - remaining program lines
    Returns: TestOperation
    """
    test_divisor_re = re.compile(r".*Test: divisible by (\d+)$")
    match = test_divisor_re.findall(lines[0])
    assert match
    divisor = int(match[0])
    true_re = re.compile(r".*If true: throw to monkey (\d+)$")
    match = true_re.findall(lines[1])
    assert match
    true_monkey = int(match[0])

    false_re = re.compile(r".*If false: throw to monkey (\d+)")
    match = false_re.findall(lines[2])
    assert match
    false_monkey = int(match[0])

    return TestOperation(divisor, true_monkey, false_monkey)


def parse_starting_items(lines: List[str]) -> List[int]:
    """
    Parse the next line into the list of starting items for the monkey
    Params: lines - remaining lines
    Returns: None
    """
    starting_items_re = re.compile(r"Starting items: (.*)$")
    match = starting_items_re.findall(lines[0])
    assert match
    items = [int(f) for f in match[0].split(",")]
    return items


class Monkey:
    """
    Monkey abstraction
    """

    def __init__(
        self,
        item_worries: List[int],
        expression: Expression,
        test_operation: TestOperation,
    ) -> None:
        """
        Constructor for the monkey object
        Params:
            item_worries: initial worry level for each item
            expression: expression that details how the worry level
                        for an item changes on inspection
            test_operation: The test operation this monkey applies
        """
        self.item_worries = item_worries
        self.expression = expression
        self.test_operation = test_operation
        self.total_inspections = 0

    def inspect(
        self,
        all_monkeys: Dict[int, "Monkey"],
        worry_drop: int,
        modulus: int,
    ) -> None:
        """
        This monkey inspects each of the items in its possession in order of
        receipt. To avoid growing integers without bounds, after calculating
        the new value, the modulus is applied to reduce the value without
        changing the mathematics.
        Params:
            all_monkeys: Dictionary mapping a monkey index to a monkey
            worry_drop: The mount of decrease in the worry after inspection
            modulus: Product of all monkey test operation divisors
        Returns: None
        """
        for old in self.item_worries:  # ignore: unused-variable
            new_val = eval(self.expression)
            new_val //= worry_drop
            new_val %= modulus
            self.test_operation.execute(new_val, all_monkeys)
            self.total_inspections += 1
        self.item_worries = []

    def __repr__(self) -> str:
        """
        Return a string representation of the monkey
        """
        return ",".join([str(item) for item in self.item_worries])


def parse_monkey(lines: List[str]) -> Tuple[int, Monkey]:
    """
    Parse all of the data associated with a given monkey
    Params:
        lines: All lines in the program
    Returns: tuple of monkey id, monkey
    """
    monkey_id_re = re.compile(r"Monkey (\d+):")
    match = monkey_id_re.findall(lines[0])
    assert match
    monkey_id = int(match[0][0])

    starting_items = parse_starting_items(lines[1:])
    worry_operation = parse_worry_operation(lines[2:])
    test_operation = parse_test_operation(lines[3:])
    return monkey_id, Monkey(starting_items, worry_operation, test_operation)


def main(fname: str, worry_drop: int, num_rounds: int) -> None:
    """
    Main function for Day11
    Params:
        fname: python
        worry_drop: Divisor indicating the drop in worry over monkey inspection
        num_rounds: The number of rounds to monitor
    Returns: None
    """
    with open(fname, "r", encoding="utf-8") as infile:
        lines = [line.rstrip("\n") for line in infile.readlines()]
        i = 0
        monkey_holdings: Dict[int, Monkey] = {}
        test_prod = 1
        while i < len(lines):
            if lines[i]:
                monkey_id, monkey = parse_monkey(lines[i:])
                monkey_holdings[monkey_id] = monkey
                test_prod *= monkey.test_operation.divisor
                i += 6
            else:
                i += 1

        monkeys = sorted(list(monkey_holdings.keys()))
        for _inspection_round in range(1, num_rounds + 1):
            for monkey_id in monkeys:
                monkey_holdings[monkey_id].inspect(
                    monkey_holdings, worry_drop, test_prod
                )
        inspections = sorted(
            [monkey_holdings[monkey_id].total_inspections for monkey_id in monkeys],
            reverse=True,
        )
        print(
            f"Most active {inspections[0]} "
            f"second {inspections[1]} "
            f"Part 1 Result {inspections[0]*inspections[1]}"
        )


if __name__ == "__main__":
    parser = ap.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("--worry-drop", default=3, type=int)
    parser.add_argument("--num-rounds", default=20, type=int)
    args = parser.parse_args()
    main(args.filename, args.worry_drop, args.num_rounds)
