import os
import time
from typing import List


script_directory = os.path.dirname(os.path.realpath(__file__))

CARD_SEQUENCE = '23456789TJQKA'

class Hand:

    cards:str = []
    hank = []
    bid:int = 0

    def __init__(self, line:str):
        # 32T3K 765
        line = line.split(' ')
        self.cards = line[0]
        self.bid = int(line[1])
        temp_hank = {}
        self.hank = []
        for c in self.cards:
            self.hank.append(CARD_SEQUENCE.index(c))
            if c not in temp_hank:
                temp_hank[c] = 0
            temp_hank[c] += 1
        self.hank = sorted(temp_hank.values(), reverse=True) + self.hank

    def __lt__(self, other:'Hand'):
        return self.hank > other.hank


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
        sorted_hands = sorted(self.hands, reverse=True)
        for index, hand in enumerate(sorted_hands):
            self.count1 += (index + 1) * hand.bid

def run():
    start_time = time.time()
    print('run')
    input_path = os.path.join(script_directory, 'input.txt')
    game = Game(input_path)
    game.calculate()
    print('part 1:', game.count1) # 248217452
    print('part 2:', game.count2) # 
    print(f'Completed in: {round(time.time() - start_time, 6)} seconds')

if __name__ == '__main__':
    print(f'starting {os.path.basename(script_directory)}')
    run()
