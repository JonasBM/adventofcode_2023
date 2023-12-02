import os
import re

script_directory = os.path.dirname(os.path.realpath(__file__))

# hack to allow for twoneighthree type of thing
number_map = {
    'one': 'one1one',
    'two': 'two2two',
    'three': 'three3three',
    'four': 'four4four',
    'five' : 'five5five',
    'six': 'six6six',
    'seven': 'seven7seven',
    'eight': 'eight8eight',
    'nine': 'nine9nine'
}


def replace_word_numbers(line:str):
    for key, value in number_map.items():
        line = line.replace(key, value)
    return line

def get_number_from_line(line:str):
    # comment next line to part one
    line = replace_word_numbers(line)
    digits_only = ''.join(re.findall(r'\d', line))
    if len(digits_only) < 1:
        raise ValueError('No digits found')
    return int(f'{digits_only[0]}{digits_only[-1]}')

def run():
    print('run')
    input_path = os.path.join(script_directory, 'input.txt')
    result = 0
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            number = get_number_from_line(line.strip().lower())
            result += number
    print('sum:', result)
    return result

if __name__ == '__main__':
    print('starting Day 01')
    run()
