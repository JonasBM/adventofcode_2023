import os
import time
import copy
from typing import List, Tuple

script_directory = os.path.dirname(os.path.realpath(__file__))


class Universe:
    filepath:str = None

    map:List[List[str]] = []
    expanded_map:List[List[str]] = []
    galaxies:List[Tuple[int, int]] = []

    count1:int = 0
    count2:int = 0

    def __init__(self, filepath:str):
        self.filepath = filepath

        self.map = []
        self.expanded_map = []
        self.galaxies = []

        self.count1 = 0
        self.count2 = 0
        self._read()


    def _read(self):
        with open(self.filepath, 'r', encoding='utf-8') as f:
            for line in f:
                self.map.append(list(line.strip()))
    
    def print(self, expanded:bool=True):
        if expanded:
            map = self.expanded_map
        else:
            map = self.map
        print('='*((len(map[0])) + 2))
        number = '0123456789' * (len(map[0])//10 + 1)
        print(' ', number[:len(map[0])])
        c = 0
        for line in map:
            print(number[c:c+1], ''.join(line))
            c += 1
        print('='*((len(map[0])) + 2))

    def create_galaxies(self):
        self.galaxies = []
        rows = len(self.expanded_map)
        cols = len(self.expanded_map[0])
        for y in range(rows):
            for x in range(cols):
                if self.expanded_map[y][x] == '#':
                    self.galaxies.append((x, y))

    def expand_universe(self, age:int):
        # for the expansion, age is used as a addition to the existing line
        # so lets just remove one for the line that already exists
        age -= 1
        self.expanded_map = copy.deepcopy(self.map)
        rows = len(self.expanded_map)
        cols = len(self.expanded_map[0])
        expand_y = list(range(rows))
        expand_x = list(range(cols))
        for y in range(rows):
            for x in range(cols):
                if self.expanded_map[y][x] == '#':
                    if x in expand_x:
                        expand_x.remove(x)
                    if y in expand_y:
                        expand_y.remove(y)
        for y in range(rows):
            for i, x in enumerate(expand_x):
                # cut = x + 1 + (i * age)
                # self.expanded_map[y] = self.expanded_map[y][:cut] + ['.']*age + self.expanded_map[y][cut:]
                for j in range(age):
                    self.expanded_map[y].insert(x + 1 + j + (i * age), '1')
        
        cols += len(expand_x) * age
        for i, y in enumerate(expand_y):
            for j in range(age):
                self.expanded_map.insert(y + 1 + j + (i * age), ['.']*cols)

    def count_distances(self, age:int=2) -> int:
        # for part 2 the expanse is by age multiplier, not add a single row/col
        # so lets treat everything as age, and use age = 2 for part one
        self.expand_universe(age)
        self.create_galaxies()
        count = 0
        galaxies = copy.deepcopy(self.galaxies)
        while galaxies:
            x, y = galaxies.pop(0)
            for _x, _y in galaxies:
                count += abs(x - _x) + abs(y - _y)
        return count

    def calculate_part1(self):
        self.count1 = self.count_distances(2)
    
    def calculate_part2(self):
        self.count2 = self.count_distances(0)
        

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
    print('part 2:', universe.count2) # 
    print(f'Completed in: {round(time.time() - start_time, 6)} seconds')

if __name__ == '__main__':
    print(f'starting {os.path.basename(script_directory)}')
    run()
