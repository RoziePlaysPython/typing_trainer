# Typing trainer TUI
My very bad typing trainer implementation on python3 using curses module
## How to use
By default this program reads from words.txt file

Each line of file is considered a sentence to type

Sentences are choosen randomly

You can specify another file to read from by adding its path as an argument: 
`python3 trainer.py /path/to/file`

Or you can run it with default settings: 
`python3 trainer.py`
## Known issues:
- May not work in other terminals, because codes for backspace and enter are different in different terminals
  - Turns out, the problem was fixed only for laptop tty, on termux the problem still persists because screen.getkey() returns '^?' in termux instead of 'KEY_BACKSPACE' as intended. I assume this problem may occur on other terminals as well
- Long strings may cause crash if they are longer, than available space
