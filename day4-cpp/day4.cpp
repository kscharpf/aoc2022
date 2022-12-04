#include <fstream>
#include <iostream>
#include <string>

bool overlap(int s1_start, int s1_end, int s2_start, int s2_end) {
  if (s1_start <= s2_start && s1_end >= s2_start) {
    return true;
  }
  return s2_start <= s1_start && s2_end >= s1_start;
}

int main(int argc, char *argv[]) {
  if (argc < 2) {
    std::cout << "Usage: " << argv[0] << " <input file>" << std::endl;
    return 0;
  }

  std::ifstream infile(argv[1]);
  std::string line;

  int overlaps = 0;
  while (std::getline(infile, line)) {
    std::string delimiter = ",";

    size_t elf_pos = line.find(delimiter);
    std::string elf1_str = line.substr(0, elf_pos);
    std::string elf2_str = line.substr(elf_pos + 1);

    std::string delimiter2 = "-";
    size_t start_stop_pos = elf1_str.find(delimiter2);
    std::string s_start = elf1_str.substr(0, start_stop_pos);
    std::string s_end = elf1_str.substr(start_stop_pos + 1);

    int elf1_start = std::stoi(s_start);
    int elf1_end = std::stoi(s_end);

    start_stop_pos = elf2_str.find(delimiter2);
    s_start = elf2_str.substr(0, start_stop_pos);
    s_end = elf2_str.substr(start_stop_pos + 1);

    int elf2_start = std::stoi(s_start);
    int elf2_end = std::stoi(s_end);

    if (overlap(elf1_start, elf1_end, elf2_start, elf2_end)) {
      overlaps++;
    }
  }

  std::cout << "Num overlaps: " << overlaps << std::endl;

  return 0;
}