import os
import time
import math
import functools
from typing import Dict


script_directory = os.path.dirname(os.path.realpath(__file__))

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

def lcd(*denominators):
    return functools.reduce(lcm, denominators)

class Network:
    filepath:str = None

    path:str = ''
    network:Dict[str, Dict[str, str]] = {}

    count1:int = 0
    count2:int = 0

    def __init__(self, filepath:str):
        self.filepath = filepath

        self.path = ''
        self.network = {}

        self.count1 = 0
        self.count2 = 0
        self._read()

    def _read(self):
        with open(self.filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            self.path = lines[0].strip()
            for line in lines[2:]:
                line = line.strip()
                if line:
                    # AAA = (BBB, CCC)
                    key, path = line.split('=')
                    key = key.strip()
                    left, right = path.split(',')
                    self.network[key] = {'L':left.strip(' ()'), 'R':right.strip(' ()')}

    def calculate(self):
        self.count1 = 0
        key = 'AAA'
        while key != 'ZZZ':
            for route in self.path:
                self.count1 += 1
                key = self.network[key][route]
                if key == 'ZZZ':
                    break

        # I was surprised that this worked, must be on purpose.
        # After the first Z encounter, the number of steps to find the next Z is the same as the first for each start.
        keys = [key for key in self.network.keys() if key.endswith('A')]
        counts = []
        count = 0
        while keys:
            for route in self.path:
                previous_length = len(keys)
                keys = [self.network[key][route] for key in keys if not key.endswith('Z')]
                if len(keys) != previous_length:
                    counts.append(count)
                count += 1
                if not keys:
                    break
        self.count2 = lcd(*counts)


def run():
    start_time = time.time()
    print('run')
    input_path = os.path.join(script_directory, 'input.txt')
    network = Network(input_path)
    network.calculate()
    print('part 1:', network.count1) # 18023
    print('part 2:', network.count2) # 14449445933179
    print(f'Completed in: {round(time.time() - start_time, 6)} seconds')

if __name__ == '__main__':
    print(f'starting {os.path.basename(script_directory)}')
    run()
