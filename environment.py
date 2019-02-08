import curses
import interpreter
import string


def main(stdscr):
    key = 0
    cursor_x = 0
    cursor_y = 0

    stdscr.clear()
    stdscr.refresh()

    curses.initscr()
    curses.curs_set(0)
    curses.start_color()

    inter = interpreter.Interpreter()

    running = True
    lines = [Line(0)]
    current = 0

    while running:
        stdscr.clear()
        l = lines[current]
        w = l.current()
        height, width = stdscr.getmaxyx()

        if key == curses.KEY_LEFT:
            if l.c == 0:  # at start of line
                if current != 0:  # not at first line
                    current -= 1  # move up a line
            else:  # move back a word
                l.c -= 1

        elif key == curses.KEY_RIGHT:
            if l.c == len(l.words) - 1:
                if current != len(lines) - 1:
                    current += 1
            else:
                l.c += 1

        if key == curses.KEY_BACKSPACE:
            if w.text == "":
                if l.c != 0:
                    del w
                    w.c -= 1
                    l = lines[current]
            else:
                w.text = w.text[:-1]

        elif chr(key) == " ":
            pos = curses.getsyx()
            newpos = pos[0], pos[1] + 1
            l.words.append(Word(newpos))
            l.c += 1
            w = l.current()

        elif chr(key) in string.printable:
            w.text += chr(key)
        x = -1
        for t in l.words:
            if t == l:
                t.update(x)
                stdscr.attron(curses.A_REVERSE)
                t.render(stdscr)
                stdscr.attroff(curses.A_REVERSE)
                x = t.end
            else:
                t.update(x)
                t.render(stdscr)
                x = t.end

        stdscr.refresh()
        key = stdscr.getch()


class Word:
    def __init__(self, c):
        self.x = c[1]
        self.y = c[0]
        self.text = ""
        self.end = self.x + len(self.text)

    def update(self, x):
        self.x = x + 1
        self.end = self.x + len(self.text)

    def render(self, stdscr):
        stdscr.addstr(self.y, self.x, self.text)


class Line:
    def __init__(self, y):
        self.y = y
        self.words = [Word((0,0))]
        self.c = 0

    def add(self, word):
        self.words.append(word)

    def current(self):
        if self.words:
            return self.words[self.c]
        else:
            return None


curses.wrapper(main)