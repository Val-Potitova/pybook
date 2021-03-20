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
    game=GameOfLife(size=(5, 5), randomize=True)
    console=Console(game)
    console.run()    
    
parser = argparse.ArgumentParser(description="data")
    parser.add_argument('-width', '--width', type=int , help='width of data')
    parser.add_argument('-height', '--height', type=int , help='height of data')
    parser.add_argument('-cellsize', '--cellsize', type=int , help='cellsize of data')
    parser.add_argument()
    
if __name__ == "__main__":
    r=int(args.width//args.cellsize)
    c=int(args.height//args.cellsize)
    life=GameOfLife((r, c), False)
    gui=GUI(life, args.cellsize, 10)
    gui.run()
