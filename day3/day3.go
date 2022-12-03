package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

func intersection(b1 []byte, b2 []byte) []byte {
	m1 := make(map[byte]bool)
	m2 := make(map[byte]bool)
	for _, c := range b1 {
		m1[c] = true
	}
	for _, c := range b2 {
		if m1[c] {
			m2[c] = true
		}
	}

	output := make([]byte, len(m2))
	i := 0
	for k := range m2 {
		output[i] = k
		i++
	}
	return output
}

func main() {
	file, err := os.Open(os.Args[1])
	if err != nil {
		log.Fatal("Error opening file")
	}

	defer file.Close()

	scanner := bufio.NewScanner(file)

	total := 0
	for scanner.Scan() {
		firstElf := scanner.Text()
		scanner.Scan()
		secondElf := scanner.Text()
		scanner.Scan()
		thirdElf := scanner.Text()
		firstElfBytes := []byte(firstElf)
		secondElfBytes := []byte(secondElf)
		thirdElfBytes := []byte(thirdElf)

		intersectBytes := intersection(firstElfBytes, secondElfBytes)
		intersectBytes = intersection(intersectBytes, thirdElfBytes)

		for _, c := range intersectBytes {
			addVal := 0
			if c >= byte('a') && c <= byte('z') {
				addVal = int(c) - int(byte('a')) + 1
			} else {
				addVal = int(c) - int(byte('A')) + 27
			}
			total += addVal
		}
	}
	fmt.Println("Total: ", total)
}
