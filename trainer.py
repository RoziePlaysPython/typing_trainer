import curses
import time
import random

class trainer:
    def __init__(self, screen, path = 'words.txt'):
        self.screen = screen
        curses.noecho()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        self.color_default = curses.color_pair(1)
        self.color_wrong = curses.color_pair(2) | curses.A_UNDERLINE
        self.color_special = curses.color_pair(3) | curses.A_BOLD

        self.startX = 7
        self.startY = 3
        self.string = self.get_string(path)
        self.string_len = len(self.string)
        self.written = ''
        self.render_text()
        self.timerow = []
        
        self.timestamp1 = time.time()
        key = self.screen.getkey()
        run = key != '\n'
        while run and self.written!=self.string:
            self.timestamp2 = time.time()
            self.timerow.append(self.timestamp2-self.timestamp1)
            backspace_pressed = 0
            self.screen.clear()
            if key == 'KEY_BACKSPACE' and len(self.written)>0:
                self.written = self.written[:len(self.written)-1]
                backspace_pressed =1
            if key == 'KEY_BACKSPACE' and len(self.written)<=0:
                backspace_pressed =1
            if key == '\n':
                run = 0
                break
            elif not backspace_pressed:
                self.written += str(key)
            self.render_text()
            self.screen.addstr(0, 0, f'{self.written}')
            self.screen.addstr(1, 0, f'{key}')
            self.screen.refresh()
            self.timestamp1 = time.time()
            key = self.screen.getkey()
        self.screen.clear()
        cpm = round((len(self.string) / sum(self.timerow))*60, 2)
        wpm = round(cpm/5, 2)
        self.screen.addstr(0,0, f'cpm: {cpm}, wpm: {wpm}')
        self.render_graph()
        self.screen.refresh()
        self.screen.getch()

    def get_string(self, path):
        with open(path) as file:
            text = file.read().split('\n')
            text = text[:len(text)-1]
        return random.choice(text)

    #Function that loops through all existing characers and prints them with their correct colors
    def render_text(self):
        for pxl in range(max(self.string_len, len(self.written))):
            color = self.color_default
            try:
                if self.written[pxl] == self.string[pxl]:
                    color = self.color_special
                else:
                    color = self.color_wrong
            except IndexError:
                color = self.color_default
            
            # A bad piece of code, that handles case when self.written is longer than self.string
            try:
                self.screen.addch(self.startY, self.startX+pxl, self.string[pxl], color)
            except IndexError:
                color = self.color_wrong
                self.screen.addch(self.startY, self.startX+pxl, self.written[pxl], color)

    def render_graph(self):
        max_value = max(self.timerow)*100
        step = max_value/10
        for idx_time_stat in range(len(self.timerow)):
            norm_time = self.timerow[idx_time_stat]*100
            for graph_Y in range(10):
                norm_time = norm_time - step
                if norm_time<=0:
                    self.screen.addch(self.startY + graph_Y, self.startX + idx_time_stat, '█', self.color_special)
                else:
                    self.screen.addch(self.startY + graph_Y, self.startX + idx_time_stat, '_', self.color_wrong)


if __name__ == '__main__':
    from sys import argv
    if len(argv) > 1:
        curses.wrapper(trainer, argv[1])
    else:
        curses.wrapper(trainer)
