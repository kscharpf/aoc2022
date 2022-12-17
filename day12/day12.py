"""
Advent of Code 2022 Day 12
"""
import argparse
from dataclasses import dataclass
from typing import List, Dict, Tuple
from collections import deque

Position = tuple[int, int]


@dataclass
class Node:
    height: int
    position: Position
    edges: List[Position]

    def __repr__(self) -> str:
        return str(self.position) + str(self.edges)


def main(fname: str) -> None:
    with open(fname, "r", encoding="utf-8") as infile:
        graph: Dict[Position, Node] = {}
        start = None
        end = None
        lines = [line.rstrip("\n") for line in infile.readlines()]
        for i, line in enumerate(lines):
            for j, c in enumerate(line):
                if c == "S":
                    height = ord("a")
                elif c == "E":
                    height = ord("z")
                else:
                    height = ord(c)
                graph[(i, j)] = Node(height, (i, j), [])
                if c == "S":
                    start = graph[(i, j)]
                elif c == "E":
                    end = graph[(i, j)]
        print(graph)
        for i in range(len(lines)):
            for j in range(len(lines[0])):
                height = graph[(i, j)].height
                next_col = (i, j + 1)
                prev_col = (i, j - 1)
                next_row = (i + 1, j)
                prev_row = (i - 1, j)
                if next_col in graph:
                    if graph[next_col].height <= height + 1:
                        graph[(i, j)].edges.append(next_col)
                if next_row in graph:
                    if graph[next_row].height <= height + 1:
                        graph[(i, j)].edges.append(next_row)
                if prev_row in graph:
                    if graph[prev_row].height <= height + 1:
                        graph[(i, j)].edges.append(prev_row)
                if prev_col in graph:
                    if graph[prev_col].height <= height + 1:
                        graph[(i, j)].edges.append(prev_col)

        assert start is not None
        assert end is not None
        q: deque[Tuple[Node, int]] = deque()
        q.append((start, 0))

        visited: List[Position] = []

        while q:
            next_node, moves = q.popleft()
            if next_node.position == end.position:
                print(f"Found end position: moves {moves}")
                break
            for edge in next_node.edges:
                if edge in visited:
                    continue
                visited.append(edge)
                q.append((graph[edge], moves + 1))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    main(args.filename)
