#include <fstream>
#include <iostream>
#include <set>
#include <vector>

int main(int argc, char *argv[]) {
  if (argc < 2) {
    std::cout << "Usage: " << argv[0] << " <test file> " << std::endl;
    return 0;
  }
  std::ifstream infile(argv[1]);

  std::string line;
  int total = 0;
  while (std::getline(infile, line)) {
    std::vector<char> v(line.size());
    std::vector<char> v2(line.size());
    std::set<char> first_elf(line.begin(), line.end());
    std::getline(infile, line);
    std::set<char> second_elf(line.begin(), line.end());
    std::getline(infile, line);
    std::set<char> third_elf(line.begin(), line.end());

    std::set_intersection(first_elf.begin(), first_elf.end(),
                          second_elf.begin(), second_elf.end(), v.begin());

    std::vector<char>::iterator it = std::set_intersection(
        v.begin(), v.end(), third_elf.begin(), third_elf.end(), v2.begin());

    for (int i = 0; i < (it - v2.begin()); i++) {
      char c = v2[i];
      if (c >= 'a' && c <= 'z') {
        total += (c - 'a' + 1);
      } else {
        total += (c - 'A' + 27);
      }
    }
  }
  std::cout << "total: " << total << std::endl;

  return 0;
}