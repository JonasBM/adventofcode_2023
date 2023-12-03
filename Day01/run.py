import os


script_directory = os.path.dirname(os.path.realpath(__file__))

number_map = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five' : '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}

def replace_word_numbers(line:str):
    for key, value in number_map.items():
        line = line.replace(key, value)
    return line

def get_dirgit_from_word(line:str, i:int, reverse=False) -> str:
    for key, value in number_map.items():
        if reverse:
            start, end = i - len(key) + 1, i + 1
        else:
            start, end = i, i + len(key)
        if line[start:end] == key:
            return value
    return None

def get_digits(line:str, reverse=False) -> (str, str):
    part1 = None
    part2 = None
    if reverse:
        start, end, step = len(line) - 1, -1, -1
    else:
        start, end, step = 0, len(line), 1
    for i in range(start, end, step):
        if line[i].isdigit():
            part1 = line[i]
            if part2 is None:
                part2 = line[i]
        if part2 is None:
            part2 = get_dirgit_from_word(line, i, reverse)
        if part1 is not None and part2 is not None:
            return part1, part2
    raise ValueError('No digits found')


def get_numbers_from_line(line:str) -> (int, int):
    first1, first2 = get_digits(line)
    last1, last2 = get_digits(line, reverse=True)
    return int(f'{first1}{last1}'), int(f'{first2}{last2}')

def run():
    print('run')
    input_path = os.path.join(script_directory, 'input.txt')
    result1 = 0
    result2 = 0
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            number1, number2 = get_numbers_from_line(line.strip().lower())
            result1 += number1
            result2 += number2
    print('part 1:', result1) # 53334
    print('part 2:', result2) # 52834

if __name__ == '__main__':
    print('starting Day 01')
    run()