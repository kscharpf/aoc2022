import argparse as ap
from typing import Tuple, List, Dict, Optional


class FileSystemNode:
    def __init__(self, name: str, sz: int, level: int, ftype: str) -> None:
        self.name = name
        self.sz = sz
        self.directories: Dict[str, Optional[DirectoryNode]] = {}
        self.cd_directories: Dict[str, Optional[DirectoryNode]] = {}
        self.files: List[FileNode] = []
        self.level = level
        self.ftype = ftype

    def add_directory(self, dirname: str) -> None:
        assert False

    def add_file(self, fname: str, sz: int) -> None:
        assert False

    def walk_dirs(self) -> List["DirectoryNode"]:
        all_dirs: List["DirectoryNode"] = []
        for d in self.cd_directories.values():
            if d and d.ftype == "DIR":
                all_dirs.append(d)
                all_dirs.extend(d.walk_dirs())
        return all_dirs

    def size(self) -> int:
        return (
            self.sz
            + sum([f.size() for f in self.files])
            + sum([d.size() if d else 0 for d in self.cd_directories.values()])
        )

    def __repr__(self) -> str:
        return " " * self.level + f"{self.ftype}: {self.name} SZ {self.size()}"


class FileNode(FileSystemNode):
    def __init__(self, name: str, sz: int, level: int) -> None:
        super().__init__(name, sz, level, "FILE")


class DirectoryNode(FileSystemNode):
    def __init__(
        self, name: str, parent: Optional["DirectoryNode"], level: int
    ) -> None:
        super().__init__(name, 0, level, "DIR")
        self.parent = parent
        self.directories["."] = self
        self.directories[name] = self
        self.directories[".."] = parent

    def add_directory(self, dirname: str) -> None:
        self.cd_directories[dirname] = DirectoryNode(dirname, self, self.level + 1)
        self.directories[dirname] = self.cd_directories[dirname]

    def add_file(self, fname: str, sz: int) -> None:
        self.files.append(FileNode(fname, sz, self.level))


def change_directory(dnode: DirectoryNode, newdir: str) -> Optional[DirectoryNode]:
    print(f"Process change_directory from {dnode.name} to {newdir}")
    if newdir == ".":
        return dnode
    if newdir == "..":
        assert dnode is not None
        return dnode.parent
    return dnode.directories[newdir]


def process_ls(
    current_directory: DirectoryNode, lines: List[str], current_line: int
) -> int:
    print(f"Process ls for {current_directory.name}")
    current_line += 1
    while current_line < len(lines):
        line = lines[current_line]
        fields = line.split(" ")
        if fields[0] == "$":
            return current_line
        if fields[0] == "dir":
            print(f"Add directory {fields[1]}")
            current_directory.add_directory(fields[1])
        else:
            print(f"Add file {fields[1]} {fields[0]}")
            current_directory.add_file(fields[1], int(fields[0]))
        current_line += 1
    return current_line


def process_command(
    current_directory: Optional[DirectoryNode], lines: List[str], current_line: int
) -> Tuple[int, Optional[DirectoryNode]]:
    assert current_directory is not None

    line = lines[current_line]
    fields = line.split(" ")
    assert fields[0] == "$"
    if fields[1] == "cd":
        current_directory = change_directory(current_directory, fields[2])
        return current_line + 1, current_directory
    assert fields[1] == "ls"
    next_line = process_ls(current_directory, lines, current_line)
    return next_line, current_directory


def main(fname: str) -> None:
    with open(fname, "r", encoding="utf-8") as infile:
        lines = [line.rstrip("\n") for line in infile.readlines()]
        current_line = 0
        root_directory: Optional[DirectoryNode] = DirectoryNode("/", None, 0)
        current_directory = root_directory

        while current_line < len(lines):
            current_line, current_directory = process_command(
                current_directory, lines, current_line
            )

        assert root_directory is not None
        all_dirs = root_directory.walk_dirs() + [root_directory]

        total = 0
        for d in all_dirs:
            if d.size() < 100000:
                total += d.size()
            print(f"DIR {d.name}: Sz {d.size()}")
        print(f"Part1 Total {total}")

        unused_space = 70000000 - root_directory.size()
        if unused_space < 30000000:
            needed_space = 30000000 - unused_space
            print(f"Unused: {unused_space} needed {needed_space}")
            best_size = -1
            best_dir: str = ""
            for d in all_dirs:
                if d.size() >= needed_space:
                    if best_size == -1 or d.size() < best_size:
                        best_dir = d.name
                        best_size = d.size()
            print(f"Best dir: {best_dir} needed {needed_space} has {best_size}")


if __name__ == "__main__":
    parser = ap.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    main(args.filename)
