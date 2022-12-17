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
    """
    Simple abstraction of a Node in the graph
    """

    height: int
    position: Position
    edges: List[Position]


Graph = dict[Position, Node]
StartNodes = List[Node]
EndNode = Node


def best_trail(graph: Graph, potential_starts: StartNodes, end: EndNode) -> None:
    """
    Find the best trail given an elevation graph, a list of potential starting
    points for the trail, and the desired end point.

    Params:
        graph: Dict[Position, Node]
        potential_starts: list of potential starting nodes (height 'a')
        end: desired end node
    Returns: None
    """

    best_moves = -1
    best_start = None

    for start in potential_starts:
        my_queue: deque[Tuple[Node, int]] = deque()
        my_queue.append((start, 0))

        visited: List[Position] = []

        while my_queue:
            next_node, moves = my_queue.popleft()
            if next_node.position == end.position:
                print(f"Found end position: moves {moves} from start {start}")
                if moves < best_moves or best_moves < 0:
                    best_moves = moves
                    best_start = start
                break
            for edge in next_node.edges:
                if edge in visited:
                    continue
                visited.append(edge)
                my_queue.append((graph[edge], moves + 1))
    assert best_start is not None
    print(f"Best Moves {best_moves} from starting position {best_start}")


HEIGHT_MAP = {"S": ord("a"), "E": ord("z")}


def build_nodes(lines: List[str], part2: bool) -> Tuple[Graph, StartNodes, EndNode]:
    """
    Create all nodes from the text input

    Params:
        lines: list of strings defining the heights of all positions
        part2: consider multiple possible starting points
    Returns:
        Tuple of node graph, list of starting nodes, and the end node
    """
    end = None
    all_starts: StartNodes = []
    graph: Graph = {}
    for i, line in enumerate(lines):
        for j, my_char in enumerate(line):
            height = HEIGHT_MAP.get(my_char, ord(my_char))
            graph[(i, j)] = Node(height, (i, j), [])
            if my_char == "E":
                end = graph[(i, j)]
            if (part2 and graph[(i, j)].height == ord("a")) or my_char == "S":
                all_starts.append(graph[(i, j)])
    assert end is not None
    return graph, all_starts, end


def build_edges(graph: Graph) -> None:
    """
    Add all edges to the graph

    Params:
        graph: all nodes in the hiking terrain
    Returns: None
    """
    num_rows = max(position[0] for position in graph.keys()) + 1
    num_cols = max(position[1] for position in graph.keys()) + 1

    print(f"Num rows {num_rows} Cols {num_cols}")

    for i in range(num_rows):
        for j in range(num_cols):
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


def main(fname: str, part2: bool) -> None:
    """
    Program entry

    Params:
        fname: filename
        part2: Search for the best starting point from all possible
    Returns:
        None
    """
    with open(fname, "r", encoding="utf-8") as infile:
        graph: Dict[Position, Node] = {}

        all_starts: List[Node] = []
        end = None
        lines = [line.rstrip("\n") for line in infile.readlines()]
        graph, all_starts, end = build_nodes(lines, part2)

        assert end is not None

        build_edges(graph)
        best_trail(graph, all_starts, end)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("--part2", action="store_true")
    args = parser.parse_args()

    main(args.filename, args.part2)
