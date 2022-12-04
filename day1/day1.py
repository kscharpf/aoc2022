'''
AOC 2022 Day 1 solution
'''
import sys

def main(fname: str) -> None:
    '''
    Part 2 Main
    '''
    with open(fname, "r", encoding="utf-8") as infile:
        lines = infile.readlines()

        elf_totals = []
        total = 0
        index = 1
        for line in lines:
            try:
                cval = int(line)
                total += cval
            except ValueError:
                elf_totals.append(total)
                elf_totals = sorted(elf_totals, reverse=True)[:3]
                index += 1
                total = 0
        if total > 0:
            elf_totals.append(total)
            elf_totals = sorted(elf_totals, reverse=True)[:3]

        print(f"Totals: {elf_totals} sum {sum(elf_totals)}")


if __name__ == "__main__":
    main(sys.argv[1])
