import argparse as ap
from dataclasses import dataclass
from typing import List, Tuple, Dict, Set
import re
import math


@dataclass
class Expression:
    eval_str: str


def parse_worry_operation(lines: List[str]) -> Expression:
    print(f"Parse worry operation: {lines[0]}")
    worry_re = re.compile(r".*Operation: new = (.*)$")
    match = worry_re.findall(lines[0])
    assert match
    print(f"Match {match}")
    expr_str = match[0]
    return Expression(expr_str)


@dataclass
class TestOperation:
    divisor: int
    throw_true_monkey: int
    throw_false_monkey: int

    def divisible(self, worry: int) -> bool:
        return worry % self.divisor == 0

    def execute(self, worry: int, all_monkeys: Dict[int, "MonkeyHolding"]) -> None:
        if self.divisible(worry):
            # print(f"Test of worry {worry} true - throwing to {self.throw_true_monkey} divisor {self.divisor}")
            all_monkeys[self.throw_true_monkey].add_item(worry)
        else:
            # print(f"Test of worry {worry} false - throwing to {self.throw_false_monkey} divisor {self.divisor}")
            all_monkeys[self.throw_false_monkey].add_item(worry)


def parse_test_operation(lines: List[str]) -> TestOperation:
    test_divisor_re = re.compile(r".*Test: divisible by (\d+)$")
    print(f"parse_test_operation for line {lines[0]}")
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
    starting_items_re = re.compile(r"Starting items: (.*)$")
    match = starting_items_re.findall(lines[0])
    assert match
    items = [int(f) for f in match[0].split(",")]
    return items


class MonkeyHolding:
    def __init__(
        self,
        item_worries: List[int],
        expression: Expression,
        test_operation: TestOperation,
    ) -> None:
        self.item_worries = item_worries
        self.expression = expression
        self.test_operation = test_operation
        self.total_inspections = 0

    def add_item(self, item: int) -> None:
        self.item_worries.append(item)

    def inspect(
        self, all_monkeys: Dict[int, "MonkeyHolding"], worry_drop: int, modulus: int,
    ) -> None:
        for old in self.item_worries:  # ignore: unused-variable
            new_val = eval(self.expression.eval_str)
            new_val //= worry_drop
            new_val %= modulus
            # print(f"Inspecting item {old} new value {new_val}")
            self.test_operation.execute(new_val, all_monkeys)
            self.total_inspections += 1
        self.item_worries = []

    def __repr__(self) -> str:
        return ",".join([str(item) for item in self.item_worries])


def parse_monkey(lines: List[str]) -> Tuple[int, MonkeyHolding]:
    monkey_id_re = re.compile(r"Monkey (\d+):")
    match = monkey_id_re.findall(lines[0])
    assert match
    monkey_id = int(match[0][0])

    starting_items = parse_starting_items(lines[1:])
    worry_operation = parse_worry_operation(lines[2:])
    test_operation = parse_test_operation(lines[3:])
    return monkey_id, MonkeyHolding(starting_items, worry_operation, test_operation)


def main(fname: str, worry_drop: int, num_rounds: int) -> None:
    with open(fname, "r", encoding="utf-8") as infile:
        lines = [line.rstrip("\n") for line in infile.readlines()]
        i = 0
        monkey_holdings: Dict[int, MonkeyHolding] = {}
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
                monkey_holdings[monkey_id].inspect(monkey_holdings, worry_drop, test_prod)
            # print("------------------------------------")
            # print(f"Results after round {inspection_round}")
            # print("------------------------------------")
            # for monkey_id in monkeys:
            # print(f"Monkey {monkey_id}: {monkey_holdings[monkey_id]}")
        inspections = sorted(
            [monkey_holdings[monkey_id].total_inspections for monkey_id in monkeys],
            reverse=True,
        )
        print(
            f"Most active {inspections[0]} second {inspections[1]} Part 1 Result {inspections[0]*inspections[1]}"
        )


if __name__ == "__main__":
    parser = ap.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("--worry-drop", default=3, type=int)
    parser.add_argument("--num-rounds", default=20, type=int)
    args = parser.parse_args()
    main(args.filename, args.worry_drop, args.num_rounds)
