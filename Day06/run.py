import os
import time
import math

from typing import List, Tuple


script_directory = os.path.dirname(os.path.realpath(__file__))

class Race:
    race_time:int = 0 # milliseconds
    distance:int = 0 # millimeters
    speed:int = 0 # millimeters per milliseconds

    def __init__(self, race_time:int, distance:int):
        self.race_time = race_time
        self.distance = distance
        self.speed = 0

    def get_button_time(self) -> Tuple[int, int]:
        # each milliseconds hold button gives 1 millimeters per milliseconds
        # - X ** 2 + race_time * X  - distance = 0
        # a = -1
        # b = race_time
        # c = -distance
        delta = self.race_time ** 2 - 4 * self.distance
        if delta < 0:
            raise ValueError('Invalid Race, delta < 0')
        delta_root = delta ** 0.5
        x1 = (self.race_time + delta_root) / 2
        x2 = (self.race_time - delta_root) / 2
        x1, x2 = min(x1, x2), max(x1, x2)
        _x1, _x2 = math.ceil(x1), math.floor(x2)
        if _x1 == x1:
            _x1 += 1
        if _x2 == x2:
            _x2 -= 1
        return _x1, _x2


class Races:
    filepath:str = None
    races:List[Race] = []
    count1:int = 0
    count2:int = 0

    def __init__(self, filepath:str):
        self.filepath = filepath
        self.races = []
        self.count1 = 0
        self.count2 = 0
        self._read()

    def _read(self):
        with open(self.filepath, 'r', encoding='utf-8') as f:
            times = []
            distances = []
            for line in f:
                line = line.strip().lower()
                if line.startswith('time'):
                    times = [int(n) for n in line.split(':')[1].strip().split(' ') if n]
                elif line.startswith('distance'):
                    distances = [int(n) for n in line.split(':')[1].strip().split(' ') if n]
            if len(times) != len(distances):
                raise ValueError('Invalid input')
            for race_time, distance in zip(times, distances):
                self.races.append(Race(race_time, distance))

    def calculate(self):
        self.count1 = 1
        for race in self.races:
            x1, x2 = race.get_button_time()
            self.count1 *= x2 - x1 + 1

def run():
    start_time = time.time()
    print('run')
    input_path = os.path.join(script_directory, 'input.txt')
    races = Races(input_path)
    races.calculate()
    print('part 1:', races.count1) # 2344708
    print('part 2:', races.count2) # 0
    print(f'Completed in: {round(time.time() - start_time, 6)} seconds')

if __name__ == '__main__':
    print('starting Day 06')
    run()
