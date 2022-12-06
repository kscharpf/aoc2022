import argparse as ap
from typing import List


def part1_main(line: str) -> None:
    last_four: List[str] = []
    for i, c in enumerate(line):
        last_four.insert(0, c)
        if len(last_four) > 4:
            last_four.pop()
        if len(set(last_four)) == 4:
            print(f"Data Sync Position found: {i+1}")
            break


def part2_main(line: str) -> None:
    last_fourteen: List[str] = []
    for i, c in enumerate(line):
        last_fourteen.insert(0, c)
        if len(last_fourteen) > 14:
            last_fourteen.pop()
        if len(set(last_fourteen)) == 14:
            print(f"Message Starc Position found: {i+1}")
            break


def main(fname: str) -> None:
    with open(fname, "r", encoding="utf-8") as infile:
        lines = [line.rstrip("\n") for line in infile.readlines()]
        for line in lines:
            part1_main(line)
            part2_main(line)


if __name__ == "__main__":
    parser = ap.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    main(args.filename)
