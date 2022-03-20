import curses
import time
import random

class trainer:
    def __init__(self, screen):
        curses.noecho()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        color_default = curses.color_pair(1)
        color_wrong = curses.color_pair(2) | curses.A_UNDERLINE
        color_special = curses.color_pair(3) | curses.A_BOLD

        self.screen = screen
        self.startX = 7
        self.startY = 3
        self.path = 'words.txt'
        self.string = self.get_string()
        self.screen.clear()
        self.screen.addstr(self.startY, self.startX, self.string, color_default)
        self.screen.refresh()
        key = self.screen.getch()
        self.written_string = ''
        while chr(key) != '' and self.written_string != self.string:
            self.screen.clear()
            self.written_string = self.string_written(self.written_string, key)
            self.correct_string = self.string_correct(self.written_string, self.string)
            self.screen.addstr(self.startY, self.startX, self.string, color_default)
            self.screen.addstr(self.startY, self.startX, self.written_string, color_wrong)
            self.screen.addstr(self.startY, self.startX, self.correct_string, color_special)
            key = self.screen.getch()
            self.screen.refresh()
    
    def get_string(self):
        with open(self.path) as word_file:
            words = word_file.read().split('\n')
            string = random.choice(words[:len(words)-1])
        return string

    def string_written(self, string, key):
        if chr(key) == 'ć':
            string = string[:len(string)-1]
            return string
        if chr(key) == '\n':
            return string
        string = string+chr(key)
        return string

    def string_correct(self, string, correct_string):
        for letter in range(len(string)):
            if string[letter] == correct_string[letter]:
                pass
            else:
                return string[:letter]
        return string[:letter+1]
        

curses.wrapper(trainer)
