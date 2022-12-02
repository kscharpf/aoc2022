package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
	"sort"
	"strconv"
)

func main() {
	file, err := os.Open(os.Args[1])
	if err != nil {
		log.Fatal("Error opening file")
	}

	defer file.Close()

	scanner := bufio.NewScanner(file)

	elfTotals := make([]int, 0)
	total := 0
	for scanner.Scan() {
		line := scanner.Text()
		value, err := strconv.Atoi(line)
		if err != nil {

			elfTotals = append(elfTotals, total)
			sort.Sort(sort.Reverse(sort.IntSlice(elfTotals)))
			elfTotals = elfTotals[:int(math.Min(3, float64(len(elfTotals))))]

			total = 0
			continue
		}
		total += value
	}

	sumTotal := 0
	for _, val := range elfTotals {
		sumTotal += val
	}
	fmt.Println("Total: ", sumTotal)
}
