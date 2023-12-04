import os
from typing import List

script_directory = os.path.dirname(os.path.realpath(__file__))

class Card:

    card_number:int = None
    winning_numbers:List[int] = []
    my_numbers:List[int] = []

    def __init__(self, line:str) -> None:
        # Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
        # Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
        split_line = line.split(':')
        self.card_number = int(split_line[0].split(' ')[-1])
        winning_numbers, my_numbers = split_line[1].split('|')
        self.winning_numbers = [int(n) for n in winning_numbers.split(' ') if n]
        self.winning_numbers.sort()
        self.my_numbers = [int(n) for n in my_numbers.split(' ') if n]
        self.my_numbers.sort()

    def calculate_score(self) -> int:
        score = 0
        for number in self.winning_numbers:
            if number in self.my_numbers:
                if score == 0:
                    score = 1
                else:
                    score *= 2
        return score


def run():
    print('run')
    input_path = os.path.join(script_directory, 'input.txt')
    result_part1 = 0
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            card = Card(line.strip().lower())
            result_part1 += card.calculate_score()
    print('part 1:', result_part1) # 23673
    print('part 2:', ) # 

if __name__ == '__main__':
    print('starting Day 04')
    run()
