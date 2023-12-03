import os
import re
from typing import List, Tuple

script_directory = os.path.dirname(os.path.realpath(__file__))

# Should have make a Game class, but I didn't =D

# 12 red cubes, 13 green cubes, and 14 blue cubes
bag = (12, 13, 14)

def get_game_number(game_line:str):
    # game 1
    try:
        return int(game_line.replace('game', '').strip())
    except ValueError as ex:
        raise ValueError(f'No game number found on: {game_line}') from ex

def get_game_sets(sets_line:str) -> List[Tuple[int, int, int]]:
    # 9 red, 2 green, 13 blue; 10 blue, 2 green, 13 red; 8 blue, 3 red, 6 green
    sets = sets_line.split(';')
    result_sets = []
    for _set in sets:
        r, g, b = 0, 0, 0
        colors = _set.split(',')
        for color in colors:
            if 'red' in color:
                r = int(color.replace('red', '').strip())
            if 'green' in color:
                g = int(color.replace('green', '').strip())
            if 'blue' in color:
                b = int(color.replace('blue', '').strip())
        result_sets.append((r,g,b))
    return result_sets

def get_game_from_line(line:str):
    # game 1: 9 red, 2 green, 13 blue; 10 blue, 2 green, 13 red; 8 blue, 3 red, 6 green
    game = line.split(':')
    return get_game_number(game[0]), get_game_sets(game[1])

def validate_game(game: List[Tuple[int, int, int]]):
    # return game number if valid, else 0
    for _set in game[1]:
        if sum(_set) > (sum(bag)):
            return 0
        for index, color in enumerate(bag):
            if _set[index] > color:
                return 0
    return game[0]

def get_fewest_cubes_from_line(game: List[Tuple[int, int, int]]):
    r, g, b = 0, 0, 0
    for _set in game[1]:
        if _set[0] > r:
            r = _set[0]
        if _set[1] > g:
            g = _set[1]
        if _set[2] > b:
            b = _set[2]
    return r * g * b

def get_result_from_line(line:str):
    game = get_game_from_line(line)
    return validate_game(game), get_fewest_cubes_from_line(game)

def run():
    print('run')
    input_path = os.path.join(script_directory, 'input.txt')
    result_part1 = 0
    result_part2 = 0
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            game_result1, game_result2 = get_result_from_line(line.strip().lower())
            result_part1 += game_result1
            result_part2 += game_result2
    print('part 1:', result_part1) # 2283
    print('part 2:', result_part2) # 78669

if __name__ == '__main__':
    print('starting Day 02')
    run()
