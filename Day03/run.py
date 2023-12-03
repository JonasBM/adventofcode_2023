import os
from typing import List

script_directory = os.path.dirname(os.path.realpath(__file__))

class Schematic:

    filepath:str = None
    matrix:List[str] = []
    count1:int = 0
    count2:int = 0
    rows:int = 0
    columns:int = 0

    def __init__(self, filepath:str) -> None:
        self.filepath = filepath
        self.matrix = []
        self.count1 = 0
        self.count2 = 0
        self.rows = 0
        self.columns = 0
        self._read()

    def _read(self):
        with open(self.filepath, 'r', encoding='utf-8') as f:
            for line in f:
                self.matrix.append(line.strip().lower())
        self.rows = len(self.matrix)
        self.columns = len(self.matrix[0])

    def count_part_numbers(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self._is_simbol(self.matrix[i][j]):
                    self._find_parts_coords(i, j)

    def _find_parts_coords(self, i:int, j:int):
        i_list = [i-1, i, i+1]
        j_list = [j-1, j, j+1]
        _parts = []
        for aux_i in i_list:
            for aux_j in j_list:
                if self.matrix[aux_i][aux_j].isdigit():
                    part_number, start_j, end_j = self._get_adjacent_part(aux_i, aux_j)
                    if (part_number, aux_i, start_j, end_j) not in _parts:
                        _parts.append((part_number, aux_i, start_j, end_j))
        is_engine = self.matrix[i][j] == '*' and len(_parts) > 1
        gear_ratio = 1
        for part_number, _, _, _ in _parts:
            self.count1 += part_number
            if is_engine:
                gear_ratio *= part_number
        if is_engine:
            self.count2 += gear_ratio

    def _get_adjacent_part(self, i:int, j:int) -> (int, int):
        part_number = self.matrix[i][j]
        start_j = j - 1
        while self.matrix[i][start_j].isdigit():
            part_number = self.matrix[i][start_j] + part_number
            start_j -= 1
        end_j = j + 1
        while end_j < self.columns and self.matrix[i][end_j].isdigit():
            part_number += self.matrix[i][end_j]
            end_j += 1
        start_j, end_j = start_j + 1, end_j - 1
        return int(self.matrix[i][start_j:end_j+1]), start_j, end_j

    def _is_simbol(self, char:str) -> bool:
        return not char.isdigit() and char != '.'

def run():
    print('run')
    input_path = os.path.join(script_directory, 'input.txt')
    schematic = Schematic(input_path)
    schematic.count_part_numbers()
    print('part 1:', schematic.count1) # 517021 # 4361
    print('part 2:', schematic.count2) # 78669 # 467835

if __name__ == '__main__':
    print('starting Day 01')
    run()
