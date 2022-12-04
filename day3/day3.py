"""
Day3 Python solution
"""
import argparse


def p1_main(fname: str) -> None:
    """
    Part 1 solution main
    """
    with open(fname, "r", encoding="utf-8") as infile:
        lines = [line.rstrip("\n") for line in infile.readlines()]
        total = 0
        for line in lines:
            first_compartment, second_compartment = (
                line[: len(line) // 2],
                line[len(line) // 2 :],
            )
            common_chars = set(first_compartment).intersection(second_compartment)
            for mychar in common_chars:
                if "a" <= mychar <= "z":
                    total += ord(mychar) - ord("a") + 1
                else:
                    total += ord(mychar) - ord("A") + 27
        print(f"Total: {total}")


def p2_main(fname: str) -> None:
    """
    Part 2 solution main
    """
    with open(fname, "r", encoding="utf-8") as infile:
        lines = [line.rstrip("\n") for line in infile.readlines()]
        total = 0

        for i in range(0, len(lines), 3):
            first_elf = set(lines[i])
            second_elf = set(lines[i + 1])
            third_elf = set(lines[i + 2])
            common_chars = first_elf.intersection(second_elf).intersection(third_elf)
            for mychar in common_chars:
                if "a" <= mychar <= "z":
                    total += ord(mychar) - ord("a") + 1
                else:
                    total += ord(mychar) - ord("A") + 27
        print(f"Total: {total}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("--part1", action="store_true")

    args = parser.parse_args()
    if args.part1:
        p1_main(args.filename)
    else:
        p2_main(args.filename)
