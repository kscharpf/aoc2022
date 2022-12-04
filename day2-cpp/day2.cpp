#include <fstream>
#include <iostream>
#include <numeric>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>

const int ROCK = 1;
const int PAPER = 2;
const int SCIZZORS = 3;

const int WIN = 6;
const int DRAW = 3;
const int LOSE = 0;

std::unordered_map<std::string, int> MOVES = {
    {"A", ROCK}, {"B", PAPER}, {"C", SCIZZORS}};
std::unordered_map<std::string, int> RESULT = {
    {"X", LOSE}, {"Y", DRAW}, {"Z", WIN}};
std::unordered_map<int, int> ADVANTAGE = {
    {ROCK, SCIZZORS}, {SCIZZORS, PAPER}, {PAPER, ROCK}};
std::unordered_map<int, int> DISADVANTAGE = {
    {SCIZZORS, ROCK}, {PAPER, SCIZZORS}, {ROCK, PAPER}};

int main(int argc, char *argv[]) {
  if (argc < 2) {
    std::cout << "Usage: " << argv[0] << " <puzzle input>" << std::endl;
    exit(1);
  }
  std::ifstream infile(argv[1]);
  std::string line;
  int total_points = 0;
  while (std::getline(infile, line)) {
    std::vector<std::string> inputs;
    std::stringstream ss(line);
    std::string token;

    while (ss >> token) {
      inputs.push_back(token);
    }

    auto oppo_move = MOVES[inputs[0]];
    if (RESULT[inputs[1]] == DRAW) {
      total_points += oppo_move + DRAW;
    } else if (RESULT[inputs[1]] == WIN) {
      total_points += DISADVANTAGE[oppo_move] + WIN;
    } else {
      total_points += ADVANTAGE[oppo_move] + LOSE;
    }
  }
  std::cout << "Total Points: " << total_points << std::endl;

  return 0;
}