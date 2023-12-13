import os
import time
from typing import List, Tuple

script_directory = os.path.dirname(os.path.realpath(__file__))

class Universe:
    filepath:str = None

    map:List[List[str]] = []
    galaxies:List[Tuple[int, int]] = []
    expand_y:List[int] = []
    expand_x:List[int] = []

    count1:int = 0
    count2:int = 0

    def __init__(self, filepath:str):
        self.filepath = filepath

        self.map = []
        self.galaxies = []
        self.expand_y = []
        self.expand_x = []

        self.count1 = 0
        self.count2 = 0
        self._read()


    def _read(self):
        with open(self.filepath, 'r', encoding='utf-8') as f:
            for line in f:
                self.map.append(list(line.strip()))
    
    def print(self):
        print('='*((len(self.map[0])) + 2))
        number = '0123456789' * (len(self.map[0])//10 + 1)
        print(' ', number[:len(self.map[0])])
        c = 0
        for line in self.map:
            print(number[c:c+1], ''.join(line))
            c += 1
        print('='*((len(self.map[0])) + 2))

    def create_galaxies(self):
        self.galaxies = []
        rows = len(self.map)
        cols = len(self.map[0])
        for y in range(rows):
            for x in range(cols):
                if self.map[y][x] == '#':
                    self.galaxies.append((x, y))

    def expand_universe(self):
        rows = len(self.map)
        cols = len(self.map[0])
        self.expand_y = list(range(rows))
        self.expand_x = list(range(cols))
        for y in range(rows):
            for x in range(cols):
                if self.map[y][x] == '#':
                    if x in self.expand_x:
                        self.expand_x.remove(x)
                    if y in self.expand_y:
                        self.expand_y.remove(y)

    def count_distances(self, age:int=1) -> int:
        age -= 1
        self.expand_universe()
        self.create_galaxies()
        count = 0
        while self.galaxies:
            x1, y1 = self.galaxies.pop(0)
            for x2, y2 in self.galaxies:
                multiplier_x = 0
                for _x in self.expand_x:
                    if x1 < _x < x2 or x2 < _x < x1:
                        multiplier_x += 1
                multiplier_y = 0
                for _y in self.expand_y:
                    if y1 < _y < y2 or y2 < _y < y1:
                        multiplier_y += 1
                count += (abs(x1 - x2) + multiplier_x * age) + (abs(y1 - y2) + multiplier_y * age)
        return count

    def calculate_part1(self):
        self.count1 = self.count_distances(2)
    
    def calculate_part2(self):
        self.count2 = self.count_distances(1000000)

    def calculate(self):
        self.calculate_part1()
        self.calculate_part2()


def run():
    start_time = time.time()
    print('run')
    input_path = os.path.join(script_directory, 'input.txt')
    universe = Universe(input_path)
    universe.calculate()
    print('part 1:', universe.count1) # 10231178
    print('part 2:', universe.count2) # 622120986954
    print(f'Completed in: {round(time.time() - start_time, 6)} seconds')

if __name__ == '__main__':
    print(f'starting {os.path.basename(script_directory)}')
    run()
