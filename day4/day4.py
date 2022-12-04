"""
Advent of Code 2022 Day 4
"""
from typing import List, Tuple
import argparse


def contains(r1: Tuple[int, int], r2: Tuple[int, int]) -> bool:
    """
    Returns true if range r2 is fully contained within r1
    """
    return r1[0] <= r2[0] and r1[1] >= r2[1]


def overlap(r1: Tuple[int, int], r2: Tuple[int, int]) -> bool:
    """
    Returns true if there is any overlap between r1 and r2
    """
    if r1[0] <= r2[0] and r1[1] >= r2[0]:
        return True
    if r1[1] >= r2[0] and r1[0] <= r2[1]:
        return True
    return False


def main(fname: str) -> None:
    """
    Main processing function
    """
    with open(fname, "r", encoding="utf-8") as infile:
        contains_count = 0
        overlap_count = 0
        for line in infile.readlines():
            elf_assignments: List[str] = line.rstrip("\n").split(",")
            ranges = []
            for assign in elf_assignments:
                range_str = assign.split("-")
                ranges.append((int(range_str[0]), int(range_str[1])))
            if contains(ranges[0], ranges[1]) or contains(ranges[1], ranges[0]):
                contains_count += 1
            if overlap(ranges[0], ranges[1]):
                overlap_count += 1
        print(f"Contains count: {contains_count}")
        print(f"Overlap count: {overlap_count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    main(args.filename)
