import argparse
def p1_main(fname):
    with open(fname, "r") as infile:
        lines = [line.rstrip("\n") for line in infile.readlines()]
        total = 0
        for line in lines:
            first_compartment, second_compartment = line[:len(line)//2], line[len(line)//2:]
            common_chars = set(first_compartment).intersection(second_compartment)
            for c in common_chars:
                if c >= 'a' and c <= 'z':
                    total += ord(c) - ord('a') + 1
                else:
                    total += ord(c) - ord('A') + 27
        print(f"Total: {total}")

def p2_main(fname):
    with open(fname, "r") as infile:
        lines = [line.rstrip("\n") for line in infile.readlines()]
        total = 0

        for i in range(0, len(lines), 3):
            first_elf = set(lines[i])
            second_elf = set(lines[i+1])
            third_elf = set(lines[i+2])
            common_chars = first_elf.intersection(second_elf).intersection(third_elf)
            for c in common_chars:
                if c >= 'a' and c <= 'z':
                    total += ord(c) - ord('a') + 1
                else:
                    total += ord(c) - ord('A') + 27
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
