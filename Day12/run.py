import os
import sys
import time
from typing import List

script_directory = os.path.dirname(os.path.realpath(__file__))


MAPPING = {'1': '#', '0': '.'}

def replace_chars(s, bits):
    bits = iter(bits)
    return ''.join(MAPPING[next(bits)] if c == '?' else c for c in s)

def print_in_same_line(s:str):
    sys.stdout.write(f"\r{s}")
    sys.stdout.flush()

class Record:

    springs:str = ''
    solution:List[int] = []
    possible_solutions:List[str] = []

    def __init__(self, line:str):
        springs, solution = line.split(' ')
        self.springs = springs
        self.solution = [int(s) for s in solution.split(',')]
        self.possible_solutions = []

    def solve(self) -> List[str]:
        self.possible_solutions = []
        indexes = [i for i, ch in enumerate(self.springs) if ch == '?']
        number_of_unknowns = len(indexes)
        for i in range(2**number_of_unknowns):
            bits = bin(i)[2:].zfill(number_of_unknowns)
            springs = replace_chars(self.springs, bits)
            _solution = [len(part) for part in springs.split('.') if part]
            if _solution == self.solution:
                self.possible_solutions.append(springs)
        return self.possible_solutions


class Records:
    filepath:str = None

    records:List[Record] = []

    count1:int = 0
    count2:int = 0

    def __init__(self, filepath:str):
        self.filepath = filepath

        self.records = []

        self.count1 = 0
        self.count2 = 0
        self._read()

    def _read(self):
        with open(self.filepath, 'r', encoding='utf-8') as f:
            for line in f:
                self.records.append(Record(line.strip()))

    def calculate_part1(self):
        self.count1 = 0
        for i, r in enumerate(self.records):
            print_in_same_line(i)
            self.count1 += len(r.solve())
        print()

    def calculate_part2(self):
        self.count2 = 0
        # this is not even close to be a solution for part 2
        # even part one takes too long
        # who knew that brute force a solution is not a good solution =D

    def calculate(self):
        self.calculate_part1()
        self.calculate_part2()


def run():
    start_time = time.time()
    print('run')
    input_path = os.path.join(script_directory, 'input.txt')
    records = Records(input_path)
    records.calculate()
    print('part 1:', records.count1) # 8193
    print('part 2:', records.count2) # 
    print(f'Completed in: {round(time.time() - start_time, 6)} seconds')


if __name__ == '__main__':
    print(f'starting {os.path.basename(script_directory)}')
    run()
