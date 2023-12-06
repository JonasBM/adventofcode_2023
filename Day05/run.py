import os
import sys
import time

from typing import List, Tuple


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
    lines:List[List[int]] = []
    offsets:List[Tuple[int,int,int]] = [] # start, end, offset

    def __init__(self, name:str):
        self.name = name
        self.lines = []
        self.offsets = []

    def add_line(self, line:str):
        self.lines.append([int(n) for n in line.strip().split(' ') if n])

    def convert(self, _in:int) -> int:
        for start, end, offset in self.offsets:
            if start <= _in < end:
                return _in + offset
        return _in
    
    def fill_offsets(self):
        self.lines.sort(key=lambda x: x[1])
        # assure it has zero to x range
        first_source_start = self.lines[0][1]
        if first_source_start != 0:
            self.lines.insert(0, [0, 0, first_source_start])
        for destination_start, source_start, length in self.lines:
            # assure range continuity
            if self.offsets and self.offsets[-1][1] != source_start:
                self.offsets.append((self.offsets[-1][1], source_start, 0))
            source_end = source_start + length
            offset = destination_start - source_start
            self.offsets.append((source_start, source_end, offset))
        # add a final range to infinity
        self.offsets.append((self.offsets[-1][1], sys.maxsize, 0))

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
        self.sections = []
        self.count1 = 0
        self.count2 = 0
        self._read()

    def _read(self):
        current_section = None
        with open(self.filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip().lower()
                if not line:
                    if current_section:
                        current_section.fill_offsets()
                    current_section = None
                elif current_section:
                    current_section.add_line(line)
                elif line.startswith('seeds'):
                    self.seeds = self._parse_seeds(line)
                else:
                    current_section = Section.get_section(line)
                    if current_section:
                        self.sections.append(current_section)
            if current_section:
                current_section.fill_offsets()
            current_section = None

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

        # this is not a pretty solution, but part 2 was too much for me, lets leave it like this
        self.count2 = sys.maxsize
        seed_ranges = [(self.seeds[i], self.seeds[i] + self.seeds[i+1]) for i in range(0, len(self.seeds), 2)]
        while seed_ranges:
            seed_start, seed_end = seed_ranges.pop()
            seed_offset = 0
            for section in self.sections:
                for start, end, offset in section.offsets:
                    if start <= seed_start and seed_end <= end:
                        seed_offset += offset
                        seed_start += offset
                        seed_end += offset
                        seed_start, seed_end = min(seed_start, seed_end), max(seed_start, seed_end)
                        break
                    if start <= seed_start < end:
                        seed_ranges.append((seed_start - seed_offset, end - seed_offset))
                    if start <= seed_end < end:
                        seed_ranges.append((start - seed_offset, seed_end - seed_offset))
                else:
                    break
            location = min(seed_start, seed_end)
            if location < self.count2:
                self.count2 = location

def run():
    start_time = time.time()
    print('run')
    input_path = os.path.join(script_directory, 'input.txt')
    plantation = Plantation(input_path)
    plantation.calculate()
    print('part 1:', plantation.count1) # 88151870
    print('part 2:', plantation.count2) # 2008785
    print('Completed in:', time.time() - start_time)
    


if __name__ == '__main__':
    print('starting Day 04')
    run()
