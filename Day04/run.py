import os
from typing import List

script_directory = os.path.dirname(os.path.realpath(__file__))

class Card:

    index:int = 0
    card_number:int = None
    winning_numbers:List[int] = []
    my_numbers:List[int] = []
    score1:int = 0
    score2:int = 0

    def __init__(self, line:str, index:int) -> None:
        self.index = index
        # Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
        # Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
        split_line = line.split(':')
        self.card_number = int(split_line[0].split(' ')[-1])
        winning_numbers, my_numbers = split_line[1].split('|')
        self.winning_numbers = [int(n) for n in winning_numbers.split(' ') if n]
        self.winning_numbers.sort()
        self.my_numbers = [int(n) for n in my_numbers.split(' ') if n]
        self.my_numbers.sort()
        self.score1 = 0
        self.score2 = 0

    def calculate_score(self) -> int:
        for number in self.winning_numbers:
            if number in self.my_numbers:
                self.score1 += 1


class Game:

    filepath:str = None
    cards:List[Card] = []
    count1:int = 0
    count2:int = 0

    def __init__(self, filepath:str) -> None:
        self.filepath = filepath
        self.cards = []
        self.count1 = 0
        self.count2 = 0
        self._read()

    def _read(self):
        with open(self.filepath, 'r', encoding='utf-8') as f:
            index = 0
            for line in f:
                self.cards.append(Card(line.strip().lower(), index))
                index += 1

    def calculate(self) -> int:
        for card in reversed(self.cards):
            card.calculate_score()
            self.count1 += 2 ** (card.score1 - 1) if card.score1 > 0 else 0
            card.score2 = 1 # count self
            if card != self.cards[-1] and card.score1 > 0:
                start = card.index + 1
                end = card.index + card.score1 + 1
                # add copy cards
                for _card in self.cards[start: end]:
                    card.score2 += _card.score2

        for card in self.cards:
            self.count2 += card.score2


def run():
    print('run')
    input_path = os.path.join(script_directory, 'input.txt')
    game = Game(input_path)
    game.calculate()
    print('part 1:', game.count1) # 23673
    print('part 2:', game.count2) # 12263631

if __name__ == '__main__':
    print('starting Day 04')
    run()
