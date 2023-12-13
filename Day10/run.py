import os
import time
from typing import List, Tuple


script_directory = os.path.dirname(os.path.realpath(__file__))

'''
| is a vertical pipe connecting north and south. │
- is a horizontal pipe connecting east and west. ─
L is a 90-degree bend connecting north and east. └
J is a 90-degree bend connecting north and west. ┘
7 is a 90-degree bend connecting south and west. ┐
F is a 90-degree bend connecting south and east. ┌
. is ground; there is no pipe in this tile.
S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
'''

class Report:
    filepath:str = None

    map:List[List[str]] = []
    start:Tuple[int, int] = None
    path:List[Tuple[int, int]] = []

    count1:int = 0
    count2:int = 0

    def __init__(self, filepath:str):
        self.filepath = filepath

        self.map = []
        self.start = None
        self.path = []

        self.count1 = 0
        self.count2 = 0
        self._read()


    def _read(self):
        with open(self.filepath, 'r', encoding='utf-8') as f:
            y = 0
            for line in f:
                line = list(line.strip())
                self.map.append(line)
                if 'S' in line:
                    self.start = (line.index('S'), y)
                y += 1

    def get_char(self, point) -> str:
        if point and point[0] < len(self.map[0]) and point[1] < len(self.map):
            return self.map[point[1]][point[0]]
        return None

    def print(self):
        print('='*(len(self.map[0])))
        for line in self.map:
            print(''.join(line).replace('|', '│').replace('-', '─').replace('L', '└').replace('J', '┘').replace('7', '┐').replace('F', '┌'))
        print('='*(len(self.map[0])))

    def get_next_point(self, point1:Tuple[int, int], point2:Tuple[int, int], prev:Tuple[int, int]) -> Tuple[int, int]:
        x1, y1 = point1
        x2, y2 = point2
        _x, _y = prev
        if x1 == _x and y1 == _y:
            return (x2, y2)
        elif x2 == _x and y2 == _y:
            return (x1, y1)
        return None

    def get_next_coords(self, point:Tuple[int, int]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        ch = self.get_char(point)
        x, y = point
        if ch == '.':
            return None
        elif ch == 'S':
            return None
        elif ch == '|':
            x1, y1 = x, y - 1
            x2, y2 = x, y + 1
        elif ch == '-':
            x1, y1 = x - 1, y
            x2, y2 = x + 1, y
        elif ch == 'L':
            x1, y1 = x, y - 1
            x2, y2 = x + 1, y
        elif ch == 'J':
            x1, y1 = x, y - 1
            x2, y2 = x - 1, y
        elif ch == '7':
            x1, y1 = x -1, y
            x2, y2 = x, y + 1
        elif ch == 'F':
            x1, y1 = x + 1, y
            x2, y2 = x, y + 1
        if any([x1 is None, y1 is None, x2 is None, y2 is None]):
            return None
        return (x1, y1), (x2, y2)

    def get_start_points(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        x, y = self.start
        x1, y1 = x, y - 1
        x2, y2 = x, y + 1
        x3, y3 = x - 1, y
        x4, y4 = x + 1, y
        results = []
        for _x, _y in [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]:
            coords = self.get_next_coords((_x, _y))
            if coords:
                (_x1, _y1), (_x2, _y2) = coords
                if _x1 == x and _y1 == y:
                    results.append(((_x, _y), (_x2, _y2)))
                elif _x2 == x and _y2 == y:
                    results.append(((_x, _y), (_x1, _y1)))
        return results
    
    def replace_start(self):
        x, y = self.start
        possible_start = '-|F7LJ'
        if self.get_char((x, y - 1)) in ('.', None, '-', 'L', 'J'):
            possible_start = possible_start.replace('|', '').replace('L', '').replace('J', '')
        if self.get_char((x, y + 1)) in ('.', None, '-', 'F', '7'):
            possible_start = possible_start.replace('|', '').replace('7', '').replace('F', '')
        if self.get_char((x - 1, y)) in ('.', None, '|', 'J', '7'):
            possible_start = possible_start.replace('-', '').replace('7', '').replace('J', '')
        if self.get_char((x + 1, y)) in ('.', None, '|', 'F', 'L'):
            possible_start = possible_start.replace('-', '').replace('F', '').replace('L', '')
        assert len(possible_start) == 1, f'Invalid start: {possible_start}'
        self.map[y][x] = possible_start

    def calculate_part1(self):
        self.count1 = 0
        self.path.append(self.start)
        start_coords = self.get_start_points()
        # I could start from both start points, and enconter in the middle, but I'm lazy
        prev, point = start_coords[0]
        self.path.append(prev)
        self.path.append(point)
        while point:
            prev = self.path[-2]
            next_points = self.get_next_coords(point)
            if not next_points or len(next_points) != 2:
                raise Exception('Invalid next points') # pylint: disable=broad-exception-raised
            point = self.get_next_point(*next_points, prev)
            if self.get_char(point) == 'S':
                break
            if point:
                self.path.append(point)
        self.count1 = len(self.path) // 2

    def calculate_part2(self):
        if not self.path:
            raise Exception('No path') # pylint: disable=broad-exception-raised
        self.count2 = 0
        columns = len(self.map[0])
        rows = len(self.map)

        # cleanup the map
        for x in range(columns):
            for y in range(rows):
                if (x, y) not in self.path:
                    self.map[y][x] = '.'
        self.replace_start()

        for y in range(rows):
            inside = False
            for x in range(columns):
                if self.map[y][x] == '.' and inside:
                    self.map[y][x] = 'I'
                    self.count2 += 1
                elif self.map[y][x] == '.' and not inside:
                    self.map[y][x] = 'O'
                elif self.map[y][x] in ('|', '7', 'F'):
                    # this is the magical part I was missing
                    # we need to pretend that the point transversing is slightly out of the center
                    # in this case I pretend that the point is below the center
                    # and so the point does not cross with L, J and -
                    inside = not inside
        # self.print()

    def calculate(self):
        self.calculate_part1()
        self.calculate_part2()


def run():
    start_time = time.time()
    print('run')
    input_path = os.path.join(script_directory, 'input.txt')
    report = Report(input_path)
    report.calculate()
    print('part 1:', report.count1) # 6768
    print('part 2:', report.count2) # 351
    print(f'Completed in: {round(time.time() - start_time, 6)} seconds')

if __name__ == '__main__':
    print(f'starting {os.path.basename(script_directory)}')
    run()
