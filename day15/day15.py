import re
import argparse
from dataclasses import dataclass, field
from typing import List, NamedTuple, Set


class Position(NamedTuple):
    x: int
    y: int


Beacon = Position
Sensor = Position


@dataclass
class BeaconExclusionZone:
    beacons: List[Beacon] = field(default_factory=list)
    beacon_map: Set[Position] = field(default_factory=set)
    sensors: List[Sensor] = field(default_factory=list)
    graph: List[List[str]] = field(default_factory=list)
    distances: List[int] = field(default_factory=list)
    min_x: int = 0
    max_x: int = 0
    min_y: int = 0
    max_y: int = 0

    def init(self) -> None:
        self.min_x = min(x for x, _ in self.beacons)
        self.min_x = min(min(x for x, _ in self.sensors), self.min_x)
        self.max_x = max(x for x, _ in self.beacons)
        self.max_x = max(max(x for x, _ in self.sensors), self.max_x)

        self.min_y = min(y for _, y in self.beacons)
        self.min_y = min(min(y for _, y in self.sensors), self.min_y)
        self.max_y = max(y for _, y in self.beacons)
        self.max_y = max(max(y for _, y in self.sensors), self.max_y)

        # self.graph = []
        # for _i in range(self.min_y, self.max_y + 1):
        # self.graph.append([])
        # self.graph[-1] = ["."] * (self.max_x - self.min_x + 1)

        # for beacon in self.beacons:
        # self.graph[beacon.y][beacon.x - self.min_x] = "B"
        # for sensor in self.sensors:
        # self.graph[sensor.y][sensor.x - self.min_x] = "S"

    def add_beacon(self, beacon: Beacon) -> None:
        self.beacons.append(beacon)
        self.beacon_map.add(beacon)

    def draw(self) -> str:
        print(
            f"Min/Max x {self.min_x}/{self.max_x} Min/Max y {self.min_y}/{self.max_y}"
        )
        ts = []
        for y in range(self.min_y, self.max_y + 1):
            ts.append("".join(self.graph[y]))
        return "\n".join(ts)

    def is_excluded(self, target_col: int, target_row: int) -> bool:
        excluded = False
        if (target_col, target_row) not in self.beacon_map:
            for sensor, threshold_distance in zip(self.sensors, self.distances):
                dist = calculate_distance(sensor, Position(target_col, target_row))

                if dist <= threshold_distance:
                    excluded = True
                    break
        return excluded

    def exclude_beacons(self, target_row: int) -> None:
        count_excluded = 0
        last_threshold_distance_delta = -1
        for x in range(self.min_x, self.max_x + 1):
            excluded = self.is_excluded(x, target_row)
            count_excluded += int(excluded)
            if excluded and x == self.min_x:
                test_x = x - 1
                while self.is_excluded(test_x, target_row):
                    test_x -= 1
                    count_excluded += 1
            if excluded and x == self.max_x:
                test_x = x + 1
                while self.is_excluded(test_x, target_row):
                    test_x += 1
                    count_excluded += 1

        print(f"Potential beacons: {count_excluded}")


def calculate_distance(p1: Position, p2: Position) -> int:
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def build_beacon_map(lines: List[str]) -> BeaconExclusionZone:

    beacon_zone = BeaconExclusionZone()

    regex = re.compile(
        r"Sensor at x=(\-?\d+), y=(\-?\d+): closest beacon is at x=(\-?\d+), y=(\-?\d+)"
    )
    for line in lines:
        match = regex.findall(line)
        assert match
        sensor = Sensor(int(match[0][0]), int(match[0][1]))
        beacon = Beacon(int(match[0][2]), int(match[0][3]))
        beacon_zone.add_beacon(beacon)
        beacon_zone.sensors.append(sensor)
        beacon_zone.distances.append(calculate_distance(sensor, beacon))
        print(f"Added beacon at {beacon}")
        print(f"Added sensor at {sensor}")
    return beacon_zone


def main(filename: str, target_row: int) -> None:
    with open(filename, "r", encoding="utf-8") as infile:
        lines = [line.rstrip("\n") for line in infile.readlines()]
        beacon_zone = build_beacon_map(lines)
        beacon_zone.init()
        # print(beacon_zone.draw())
        beacon_zone.exclude_beacons(target_row)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("--target-row", type=int, default=10)
    args = parser.parse_args()
    main(args.filename, args.target_row)
