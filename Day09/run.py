import os
import time
from typing import List


script_directory = os.path.dirname(os.path.realpath(__file__))

class Report:
    filepath:str = None

    entries:List[List[int]] = []

    count1:int = 0
    count2:int = 0

    def __init__(self, filepath:str):
        self.filepath = filepath

        self.entries = []

        self.count1 = 0
        self.count2 = 0
        self._read()

    def _read(self):
        with open(self.filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    self.entries.append([int(i) for i in line.split(' ')])

    def _get_missing_entry(self, entry:List[int]):
        next = 0
        firsts = []
        while sum(entry):
            next += entry[-1]
            firsts.append(entry[0])
            length = len(entry)
            entry = [entry[i + 1] - entry[i]  for i in range(length) if i < length - 1]
        prev = 0
        for n in reversed(firsts):
            prev = n - prev
        return prev, next

    def calculate(self):
        self.count1 = 0
        self.count2 = 0
        for entry in self.entries:
            prev, next = self._get_missing_entry(entry)
            self.count1 += next
            self.count2 += prev


def run():
    start_time = time.time()
    print('run')
    input_path = os.path.join(script_directory, 'input.txt')
    report = Report(input_path)
    report.calculate()
    print('part 1:', report.count1) # 1782868781
    print('part 2:', report.count2) # 1057
    print(f'Completed in: {round(time.time() - start_time, 6)} seconds')

if __name__ == '__main__':
    print(f'starting {os.path.basename(script_directory)}')
    run()
