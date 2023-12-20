import os
import time
from typing import List

script_directory = os.path.dirname(os.path.realpath(__file__))


class Pattern:

    pattern:List[List[str]] = None
    vertical:List[int] = None
    horizontal:List[int] = None

    def __init__(self, pattern:List[List[str]]):
        self.pattern = pattern
        self._parse_pattern()

    def _parse_pattern(self):
        self.vertical = []
        self.horizontal = []

        rows = len(self.pattern)
        cols = len(self.pattern[0])
        for y in range(rows):
            row = ''.join(self.pattern[y])
            self.horizontal.append(int(row, 2))
        for x in range(cols):
            row = (''.join([self.pattern[y][x] for y in range(rows)]))
            self.vertical.append(int(row, 2))

def find_mirror(nums:List[int]) -> int:
    result = []
    lengh = len(nums)
    mid = lengh // 2
    for i in range(1, lengh):
        if i <= mid:
            if nums[0:i] == list(reversed(nums[i:i*2])):
                result.append(i)
        else:
            if nums[i*2 - lengh:i] == list(reversed(nums[i:])):
                result.append(i)
    if not result:
        return 0
    if len(result) > 1:
        raise Exception('too many results') # pylint: disable=broad-exception-raised
    return result[0]


class Cluster:
    filepath:str = None

    patterns:List[Pattern] = []

    count1:int = 0
    count2:int = 0

    def __init__(self, filepath:str):
        self.filepath = filepath

        self.count1 = 0
        self.count2 = 0
        self._read()

    def _read(self):
        self.patterns = []
        _map = []
        with open(self.filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    _map.append(list(line.replace('.', '0').replace('#', '1')))
                else:
                    if _map:
                        self.patterns.append(Pattern(_map))
                    _map = []
            if _map:
                self.patterns.append(Pattern(_map))

    def calculate_part1(self):
        self.count1 = 0
        for pattern in self.patterns:
            self.count1 += find_mirror(pattern.horizontal)*100 + find_mirror(pattern.vertical)

    def calculate_part2(self):
        self.count2 = 0

    def calculate(self):
        self.calculate_part1()
        self.calculate_part2()


def run():
    start_time = time.time()
    print('run')
    input_path = os.path.join(script_directory, 'input.txt')
    cluster = Cluster(input_path)
    cluster.calculate()
    print('part 1:', cluster.count1) # 33356
    print('part 2:', cluster.count2) # 
    print(f'Completed in: {round(time.time() - start_time, 6)} seconds')


if __name__ == '__main__':
    print(f'starting {os.path.basename(script_directory)}')
    run()
