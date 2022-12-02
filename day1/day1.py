import sys
def main(fname):
    with open(fname, "r") as infile:
        lines = infile.readlines()

        elf_totals = []
        total = 0
        index = 1
        for line in lines:
            try:
                x = int(line)
                total += x
            except:
                elf_totals.append(total)
                elf_totals = sorted(elf_totals, reverse=True)[:3]
                index += 1
                total = 0
        print(f"Totals: {elf_totals} sum {sum(elf_totals)}")

if __name__ == "__main__":
    main(sys.argv[1])