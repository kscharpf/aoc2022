import argparse
import ast
from typing import Union, List
from enum import Enum
import functools

LESS = -1
EQUAL = 0
GREATER = 1


def compare(v1: Union[List[int], int], v2: Union[List[int], int]) -> int:
    if isinstance(v1, int) and isinstance(v2, int):
        if v1 < v2:
            return LESS
        if v1 > v2:
            return GREATER
        return EQUAL
    if isinstance(v1, list) and isinstance(v2, list):
        for x, y in zip(v1, v2):
            result = compare(x, y)
            if result == LESS:
                return LESS
            if result == GREATER:
                return GREATER
        if len(v1) < len(v2):
            return LESS
        if len(v1) > len(v2):
            return GREATER
        return EQUAL
    if isinstance(v1, list):
        return compare(v1, [v2])
    return compare([v1], v2)


def main(fname: str) -> None:
    with open(fname, "r", encoding="utf-8") as infile:
        lines = infile.readlines()
        proper_order = 0
        index_sum = 0
        i = 0
        pair_index = 1
        packets: List[Union[List, int]] = []
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
                result *= (i+1)
        print(f"Part 2: {result}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    args = parser.parse_args()
    main(args.filename)
