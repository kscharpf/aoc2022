package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	infile, err := os.Open(os.Args[1])
	if err != nil {
		fmt.Println("Failed to open file")
	}

	defer infile.Close()

	scanner := bufio.NewScanner(infile)

	scanner.Scan()
	line := scanner.Text()

	p1start := findStart(line, 4)
	p2start := findStart(line, 14)
	fmt.Println("Data Sync Start: ", p1start)
	fmt.Println("Msg Sync Start: ", p2start)
}

func findStart(line string, diffLen int) int {
	lastRunes := make([]rune, 0)
	syncPos := -1
	for i, c := range line {
		lastRunes = append(lastRunes, c)
		start := len(lastRunes) - diffLen
		if start >= 0 {
			lastRunes = lastRunes[start:]
		}
		if len(lastRunes) == diffLen {
			mymap := make(map[rune]bool)
			for _, b := range lastRunes {
				mymap[b] = true
			}
			count := 0
			for key, _ := range mymap {
				count++
				if key == -1 {
					fmt.Println("avoid warning")
				}
			}
			if count == diffLen {
				syncPos = i + 1
				break
			}
		}
	}
	return syncPos
}
