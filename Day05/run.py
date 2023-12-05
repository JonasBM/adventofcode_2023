import os
import sys
from typing import List


script_directory = os.path.dirname(os.path.realpath(__file__))

sections = [
    'seed-to-soil',
    'soil-to-fertilizer',
    'fertilizer-to-water',
    'water-to-light',
    'light-to-temperature',
    'temperature-to-humidity',
    'humidity-to-location',
]

class Section:

    name:str = None
    lines:List[str] = []

    def __init__(self, name:str):
        self.name = name
        self.lines = []

    def add_line(self, line:str):
        self.lines.append([int(n) for n in line.strip().split(' ') if n])

    def convert(self, _in:int) -> int:
        for line in self.lines:
            if line[1] <= _in <= (line[1] + line[2]):
                return _in + line[0] - line[1]
        return _in

    @classmethod
    def get_section(cls, line:str):
        # seed-to-soil map:
        line = line.replace('map:', '').strip()
        if line:
            return cls(line)
        return None

class Plantation:

    filepath:str = None
    seeds:List[int] = []

    sections:List[Section] = []

    count1:int = 0
    count2:int = 0

    def __init__(self, filepath:str):
        self.filepath = filepath
        self.seeds = []
        self.count1 = 0
        self.count2 = 0
        self._read()

    def _read(self):
        current_section = None
        with open(self.filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip().lower()
                if not line:
                    current_section = None
                elif current_section:
                    current_section.add_line(line)
                elif line.startswith('seeds'):
                    self.seeds = self._parse_seeds(line)
                else:
                    current_section = Section.get_section(line)
                    if current_section:
                        self.sections.append(current_section)

    def _parse_seeds(self, line:str) -> None:
        # seeds: 79 14 55 13
        _seeds = line.split(':')[1].strip()
        return [int(n) for n in _seeds.split(' ') if n]

    def get_location(self, _in:int) -> int:
        for section in self.sections:
            _in = section.convert(_in)
        return _in

    def calculate(self):
        self.count1 = sys.maxsize
        for seed in self.seeds:
            location = self.get_location(seed)
            if location < self.count1:
                self.count1 = location

def run():
    print('run')
    input_path = os.path.join(script_directory, 'input.txt')
    plantation = Plantation(input_path)
    plantation.calculate()
    print('part 1:', plantation.count1) # 88151870
    print('part 2:', plantation.count2) #

if __name__ == '__main__':
    print('starting Day 04')
    run()
