"""
Advent of Code Day 13
"""
import argparse
import ast
from typing import Union, List, Any
import functools

LESS = -1
EQUAL = 0
GREATER = 1

def int_compare(val1: int, val2: int) -> int:
    """
    Compare two ints
    Params:
        val1: integer
        val2: integer
    Returns: int - comparison value
    """
    if val1 < val2:
        return LESS
    if val1 > val2:
        return GREATER
    return EQUAL

def list_compare(val1: List[Any], val2: List[Any]) -> int:
    """
    Compare two lists
    Params:
        val1: list of integers
        val2: list of integers
    Returns: int - comparison
    """
    for entry1, entry2 in zip(val1, val2):
        result = compare(entry1, entry2)
        if result == LESS:
            return LESS
        if result == GREATER:
            return GREATER
    if len(val1) < len(val2):
        return LESS
    if len(val1) > len(val2):
        return GREATER
    return EQUAL


def compare(val1: Union[List[Any], int], val2: Union[List[Any], int]) -> int:
    """
    Comparison of integers and lists
    Params:
        val1: integer or list
        val2: integer or list
    Returns: Comparison value
    """
    if isinstance(val1, int) and isinstance(val2, int):
        return int_compare(val1, val2)
    if isinstance(val1, list) and isinstance(val2, list):
        return list_compare(val1, val2)
    if isinstance(val1, list):
        return compare(val1, [val2])
    return compare([val1], val2)


def main(fname: str) -> None:
    """
    Program entry
    """
    with open(fname, "r", encoding="utf-8") as infile:
        lines = infile.readlines()
        proper_order = 0
        index_sum = 0
        i = 0
        pair_index = 1
        packets: List[Union[List[Any], int]] = []
        while i < len(lines) - 1:
            left_packet = ast.literal_eval(lines[i])
            right_packet = ast.literal_eval(lines[i + 1])
            result = compare(left_packet, right_packet)
            print(f"Compare {left_packet} vs {right_packet} result {result}")
            if result == LESS:
                proper_order += 1
                index_sum += pair_index
            packets.append(left_packet)
            packets.append(right_packet)
            i += 3
            pair_index += 1

        print(f"Number of in order pairs: {proper_order}")
        print(f"Index sum {index_sum}")
        packets.append([[2]])
        packets.append([[6]])
        packets = sorted(packets, key=functools.cmp_to_key(compare))

        result = 1
        for i, packet in enumerate(packets):
            if packet in ([[2]], [[6]]):
                result *= i + 1
        print(f"Part 2: {result}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    args = parser.parse_args()
    main(args.filename)
