"""
This module processes the Day 7 Advent of Code challenge.
"""
import argparse as ap
from typing import Tuple, List, Dict, Optional
from dataclasses import dataclass


@dataclass
class FileNode:
    """
    File tree file node abstraction
    Has an explicit size but can hold no other files or directories
    """

    name: str
    file_size: int

    def size(self) -> int:
        """
        Return the file size - satisfy the callable interface
        Params: self
        Return: size of the file
        """
        return self.file_size


class DirectoryNode:
    """
    File tree directory node abstraction
    Has no intrinsic size but contains other files and directories
    """

    def __init__(self, name: str, parent: Optional["DirectoryNode"]) -> None:
        """
        Constructor for a DirectoryNode object
        Params:
            name: name of the directory
            parent: Parent object of this directory
        """
        self.name = name
        self.parent = parent
        self.directories: Dict[str, Optional["DirectoryNode"]] = {}
        self.directories["."] = self
        self.directories[name] = self
        self.directories[".."] = parent
        self.cd_directories: Dict[str, DirectoryNode] = {}
        self.files: List[FileNode] = []

    def walk_dirs(self) -> List["DirectoryNode"]:
        """
        walk_dirs returns all subdirectories recursively
        Params:
            self
        Returns: list of all subdirectories
        """
        all_dirs: List[DirectoryNode] = []
        for my_dir in self.cd_directories.values():
            all_dirs.append(my_dir)
            all_dirs.extend(my_dir.walk_dirs())
        return all_dirs

    def add_directory(self, dirname: str) -> None:
        """
        Append a directory object to this directory
        Params:
            dirname: name of the directory
        Returns: None
        """
        self.cd_directories[dirname] = DirectoryNode(dirname, self)
        self.directories[dirname] = self.cd_directories[dirname]

    def add_file(self, fname: str, f_sz: int) -> None:
        """
        Append a file object to this directory
        Params:
            fname: name of file
            sz: size of the file
        Returns: None
        """
        self.files.append(FileNode(fname, f_sz))

    def size(self) -> int:
        """
        Returns the recursive size of all nodes in this directory.
        Params: self
        Returns: size as integer
        """
        return sum(d.size() for d in list(self.cd_directories.values()) + self.files)

    def __repr__(self) -> str:
        return f"DIR {self.name}"


def change_directory(dnode: DirectoryNode, newdir: str) -> Optional[DirectoryNode]:
    """
    Process change directory command on the current directory
    Params:
        dnode: current directory object
        newdir: name of new directory
    Returns: Optional[DirectoryNode] - Directory object switched into
    """
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
    """
    Process ls command on the current directory
    Params:
        current_directory: active directory object
        lines: List of strings in the input file
        current_line: index of the line currently under process
    Returns:
        the next line index to process
    """
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
    """
    Process the next command from the input stream
    Params:
        current_directory: Directory object where the user is
        lines: All command lines in the input file
        current_line: Index of the command line currently under process
    Returns:
        Tuple[The next line to process, The new directory object]
    """
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
    """
    Main function for processing a file system command input and output stream
    Params:
        fname: Input file
    """
    with open(fname, "r", encoding="utf-8") as infile:
        lines = [line.rstrip("\n") for line in infile.readlines()]
        current_line = 0
        root_directory: Optional[DirectoryNode] = DirectoryNode("/", None)
        current_directory = root_directory

        while current_line < len(lines):
            current_line, current_directory = process_command(
                current_directory, lines, current_line
            )

        assert root_directory is not None
        all_dirs = root_directory.walk_dirs() + [root_directory]

        total = 0
        for f_dir in all_dirs:
            print(f"f_dir {f_dir}")
            if f_dir.size() < 100000:
                total += f_dir.size()
            print(f"DIR {f_dir.name}: Sz {f_dir.size()}")
        print(f"Part1 Total {total}")

        unused_space = 70000000 - root_directory.size()
        if unused_space < 30000000:
            needed_space = 30000000 - unused_space
            print(f"Unused: {unused_space} needed {needed_space}")
            best_size = -1
            best_dir: str = ""
            for f_dir in all_dirs:
                if f_dir.size() >= needed_space:
                    if best_size == -1 or f_dir.size() < best_size:
                        best_dir = f_dir.name
                        best_size = f_dir.size()
            print(f"Best dir: {best_dir} needed {needed_space} has {best_size}")


if __name__ == "__main__":
    parser = ap.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    main(args.filename)
