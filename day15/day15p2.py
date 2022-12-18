import re
import argparse
from dataclasses import dataclass, field
from typing import List, NamedTuple
from shapely import Polygon, geometry, MultiPolygon
from shapely.ops import unary_union


class Position(NamedTuple):
    x: int
    y: int


Beacon = Position
Sensor = Position


@dataclass
class BeaconExclusionZone:
    beacons: List[Beacon] = field(default_factory=list)
    sensors: List[Sensor] = field(default_factory=list)


def get_sensor_exclusion(sensor: Sensor, beacon: Beacon) -> Polygon:
    dist = abs(sensor.x - beacon.x) + abs(sensor.y - beacon.y)
    return Polygon(
        [
            (sensor.x, sensor.y + dist),
            (sensor.x - dist, sensor.y),
            (sensor.x, sensor.y - dist),
            (sensor.x + dist, sensor.y),
        ]
    )


def get_all_exclusions(sensors: List[Sensor], beacons: List[Beacon]) -> Polygon:
    exclusion_list: List[Polygon] = []
    for sensor, beacon in zip(sensors, beacons):
        exclusion_list.append(get_sensor_exclusion(sensor, beacon))
    return unary_union(exclusion_list)


def build_potential_beacon_area(
    min_x: int, min_y: int, max_x: int, max_y: int
) -> Polygon:
    return geometry.box(min_x, min_y, max_x, max_y)


def filter_excluded(full_area: Polygon, exclusion_zone: Polygon) -> Polygon:
    return full_area.difference(exclusion_zone)


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
        beacon_zone.beacons.append(beacon)
        beacon_zone.sensors.append(sensor)
        print(f"Added beacon at {beacon}")
        print(f"Added sensor at {sensor}")
    return beacon_zone


def main(filename: str, min_coord: int, max_coord: int) -> None:
    with open(filename, "r", encoding="utf-8") as infile:
        lines = [line.rstrip("\n") for line in infile.readlines()]
        beacon_zone = build_beacon_map(lines)
        exclusion_zone = get_all_exclusions(beacon_zone.sensors, beacon_zone.beacons)
        full_area = build_potential_beacon_area(
            min_coord, min_coord, max_coord, max_coord
        )
        remainder = filter_excluded(full_area, exclusion_zone)
        if isinstance(remainder, MultiPolygon):
            # example problem leaves us with a disjoint polygon
            remainder = remainder.geoms[0]
        x_center = round((remainder.bounds[0] + remainder.bounds[2]) / 2)
        y_center = round((remainder.bounds[1] + remainder.bounds[3]) / 2)
        print(remainder)
        print(x_center, y_center)
        print(x_center * 4000000 + y_center)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("--min-coord", default=0, type=int)
    parser.add_argument("--max-coord", default=4000000, type=int)
    args = parser.parse_args()
    main(args.filename, args.min_coord, args.max_coord)
