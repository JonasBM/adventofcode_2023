import os
import re
from typing import List, Tuple

script_directory = os.path.dirname(os.path.realpath(__file__))

class Schematic:

    filepath:str = None
    matrix:List[str] = []
    count1:int = 0
    rows:int = 0
    columns:int = 0

    def __init__(self, filepath:str) -> None:
        self.filepath = filepath
        self.count1 = 0
        self._read()

    def _read(self):
        with open(self.filepath, 'r', encoding='utf-8') as f:
            for line in f:
                self.matrix.append(line.strip().lower())
        self.rows = len(self.matrix)
        self.columns = len(self.matrix[0])

    def count_part_numbers(self):
        i = 0
        while i < self.rows:
            j = 0
            while j < self.columns:
                char = self.matrix[i][j]
                if char.isdigit():
                    j, part_number = self._get_part_number(i, j)
                    self.count1 += part_number
                else:
                    j += 1
            i += 1

    def _get_part_number(self, i:int, start_j:int) -> int:
        if not self.matrix[i][start_j].isdigit() or start_j == self.columns - 1:
            return start_j + 1, 0
        j = start_j + 1
        for char in self.matrix[i][j:]:
            if not char.isdigit():
                break
            j += 1
        if not self._validate_part_number(i, start_j, j - 1):
            return j, 0
        return j, int(self.matrix[i][start_j:j])

    def _validate_part_number(self, i:int, start_j:int, end_j:int) -> bool:
        if start_j > 0:
            start_j -= 1
        if end_j < self.columns - 1:
            end_j += 1

        # same line
        if self._is_simbol(self.matrix[i][start_j]):
            return True
        if end_j >= self.columns:
            if self._is_simbol(self.matrix[i][self.columns-1]):
                return True
        else:
            if self._is_simbol(self.matrix[i][end_j]):
                return True

        # one line above
        if i > 0:
            for j in range(start_j, end_j + 1):
                if self._is_simbol(self.matrix[i-1][j]):
                    return True

        # one line below
        if i < self.rows - 1:
            for j in range(start_j, end_j + 1):
                if self._is_simbol(self.matrix[i+1][j]):
                    return True
        return False

    def _is_simbol(self, char:str) -> bool:
        return not char.isdigit() and char != '.'

def run():
    print('run')
    input_path = os.path.join(script_directory, 'input.txt')
    result_part2 = 0
    schematic = Schematic(input_path)
    schematic.count_part_numbers()
    print('part 1:', schematic.count1) # 3744
    print('part 2:', result_part2) # 78669

if __name__ == '__main__':
    print('starting Day 01')
    run()
