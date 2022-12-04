package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

func overlap(e1Start int, e1End int, e2Start int, e2End int) bool {
	if e1Start <= e2Start && e1End >= e2Start {
		return true
	}
	return e2Start <= e1Start && e2End >= e1Start

}

func main() {
	infile, err := os.Open(os.Args[1])
	if err != nil {
		log.Fatal("Failed to open file: ", os.Args[1])
	}

	defer infile.Close()

	scanner := bufio.NewScanner(infile)

	overlapCount := 0

	for scanner.Scan() {
		line := scanner.Text()
		elf_assignments := strings.Split(line, ",")

		elf1_range := strings.Split(elf_assignments[0], "-")
		elf2_range := strings.Split(elf_assignments[1], "-")
		elf1_start, err := strconv.Atoi(elf1_range[0])
		if err != nil {
			log.Fatal("Unable to convert number")
		}
		elf1_end, err := strconv.Atoi(elf1_range[1])
		if err != nil {
			log.Fatal("Unable to convert number")
		}
		elf2_start, err := strconv.Atoi(elf2_range[0])
		if err != nil {
			log.Fatal("Unable to convert number")
		}
		elf2_end, err := strconv.Atoi(elf2_range[1])
		if err != nil {
			log.Fatal("Unable to convert number")
		}

		if overlap(elf1_start, elf1_end, elf2_start, elf2_end) {
			overlapCount += 1

		}
	}
	fmt.Println("Num Overlaps: ", overlapCount)

}
