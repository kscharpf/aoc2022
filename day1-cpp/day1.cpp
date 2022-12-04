#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <numeric>

int main(int argc, char *argv[]) {
  if (argc < 2) {
    std::cout << "Usage: day1 <puzzle input>" << std::endl;
    exit(1);
  }
  std::ifstream infile(argv[1]);
  std::string caloriesString;
  std::vector<int32_t> elfCalories;
  int32_t currentTotalCalories = 0;

  while (std::getline(infile, caloriesString)) {
    if (caloriesString.empty()) {
      elfCalories.push_back(currentTotalCalories);
      currentTotalCalories = 0;
    } else {
      currentTotalCalories += std::stoi(caloriesString);
    }
  }
  if (currentTotalCalories) elfCalories.push_back(currentTotalCalories);
  std::sort(elfCalories.begin(), elfCalories.end(), std::greater<int32_t>());

  std::cout << "Top 3 Calories: " << std::accumulate(elfCalories.begin(), elfCalories.begin() + 3, 0);
  return 0;
}