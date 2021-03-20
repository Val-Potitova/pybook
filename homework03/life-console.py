import curses

from life import GameOfLife
from ui import UI
import time
from time import sleep

import argparse


class Console(UI):

    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)
        self.screen = curses.initscr()

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        self.screen.border(0)

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for y, row in enumerate(self.life.curr_generation):
            for x, value in enumerate(row):
                self.sign = "*" if value == 1 else " "
                self.screen.addch(x + 1, y + 1, self.sign)

    def run(self) -> None:
        self.draw_borders()
        self.running = True
        while self.running:
            self.draw_borders()
            self.draw_grid()
            self.life.step()
            self.screen.refresh()
            time.sleep(1)
        curses.endwin()
        
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="data", prog="gof-console.py")
    parser.add_argument('--rows', type=int, default=24, help='rows of data')
    parser.add_argument('--cols', type=int, default=80, help='cols of data')
    parser.add_argument('--max_generations', type=int, default=50, help='max generations of data')
    args = parser.parse_args()
    r = args.rows > 0
    c = args.cols > 0
    m = args.max_generations > 0
    if r and c and m:
        console = Console(GameOfLife((args.rows, args.cols), max_generations=args.max_generations))
        curses.update_lines_cols()
        console.run()
    else:
        if not r:
            print('Incorrect value of rows')
        if not c:
            print('Incorrect value of cols')
        if not m:
            print('Incorrect value of max generations')
