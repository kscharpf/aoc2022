package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"
)

func main() {
	file, err := os.Open(os.Args[1])
	if err != nil {
		log.Fatal("Error opening file")
	}

	defer file.Close()

	scanner := bufio.NewScanner(file)

	ROCK := 1
	PAPER := 2
	SCIZZORS := 3

	LOSE := 0
	DRAW := 3
	WIN := 6

	MOVES := map[string]int{"A": ROCK, "B": PAPER, "C": SCIZZORS, "X": ROCK, "Y": PAPER, "Z": SCIZZORS}
	RESULT := map[string]int{"X": LOSE, "Y": DRAW, "Z": WIN}
	ADVANTAGE := map[int]int{ROCK: SCIZZORS, SCIZZORS: PAPER, PAPER: ROCK}
	DISADVANTAGE := map[int]int{SCIZZORS: ROCK, PAPER: SCIZZORS, ROCK: PAPER}

	totalPoints := 0
	for scanner.Scan() {
		line := scanner.Text()
		substrs := strings.Split(line, " ")
		oppo_move_str := substrs[0]
		my_result_str := substrs[1]
		oppo_move := MOVES[oppo_move_str]
		if RESULT[my_result_str] == DRAW {
			totalPoints += oppo_move + DRAW
		} else if RESULT[my_result_str] == WIN {
			totalPoints += DISADVANTAGE[oppo_move] + WIN
		} else {
			totalPoints += ADVANTAGE[oppo_move] + LOSE
		}
	}
	fmt.Println("Total Points: ", totalPoints)
}
