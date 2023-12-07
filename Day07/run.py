import os
import time
from typing import List
from functools import cmp_to_key


script_directory = os.path.dirname(os.path.realpath(__file__))

CARD_SEQUENCE_PART1 = '23456789TJQKA'
CARD_SEQUENCE_PART2 = 'J23456789TQKA'

class Hand:

    cards:str = []
    hank_part1 = []
    hank_part2 = []
    bid:int = 0

    def __init__(self, line:str):
        # 32T3K 765
        line = line.split(' ')
        self.cards = line[0]
        self.bid = int(line[1])
        temp_hank = {}
        self.hank_part1 = []
        self.hank_part2 = []
        for c in self.cards:
            self.hank_part1.append(CARD_SEQUENCE_PART1.index(c))
            self.hank_part2.append(CARD_SEQUENCE_PART2.index(c))
            if c not in temp_hank:
                temp_hank[c] = 0
            temp_hank[c] += 1
        self.hank_part1 = sorted(temp_hank.values(), reverse=True) + self.hank_part1
        wildcard = temp_hank.pop('J', 0)
        self.hank_part2 = sorted(temp_hank.values(), reverse=True) + self.hank_part2
        self.hank_part2[0] += wildcard

def compare_part1(a:Hand, b:Hand):
    if a.hank_part1 == b.hank_part1:
        return 0
    if a.hank_part1 > b.hank_part1:
        return 1
    return -1

def compare_part2(a:Hand, b:Hand):
    if a.hank_part2 == b.hank_part2:
        return 0
    if a.hank_part2 > b.hank_part2:
        return 1
    return -1

class Game:
    filepath:str = None

    hands: List[Hand] = []

    count1:int = 0
    count2:int = 0

    def __init__(self, filepath:str):
        self.filepath = filepath

        self.hands = []

        self.count1 = 0
        self.count2 = 0
        self._read()

    def _read(self):
        with open(self.filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    self.hands.append(Hand(line))

    def calculate(self):
        self.count1 = 0
        sorted_hands = sorted(self.hands, key=cmp_to_key(compare_part1))
        for index, hand in enumerate(sorted_hands):
            self.count1 += (index + 1) * hand.bid

        self.count2 = 0
        sorted_hands = sorted(self.hands, key=cmp_to_key(compare_part2))
        for index, hand in enumerate(sorted_hands):
            self.count2 += (index + 1) * hand.bid

def run():
    start_time = time.time()
    print('run')
    input_path = os.path.join(script_directory, 'input.txt')
    game = Game(input_path)
    game.calculate()
    print('part 1:', game.count1) # 248217452
    print('part 2:', game.count2) # 245576185
    print(f'Completed in: {round(time.time() - start_time, 6)} seconds')

if __name__ == '__main__':
    print(f'starting {os.path.basename(script_directory)}')
    run()
