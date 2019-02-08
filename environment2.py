import curses
import interpreter
import string
import math


class Item:
    def __init__(self, y, x):
        self.x = x
        self.y = y
        self.text = ""
        self.end = self.x + len(self.text)

    def update_pos(self, x):
        self.x = x + 1
        self.end = self.x + len(self.text)

    def render(self, stdscr):
        stdscr.addstr(self.y, self.x, self.text)


class Line:
    def __init__(self, y):
        self.y = y
        self.items = [Item(self.y, start_x)]
        self.current = 0
        self.cursor = start_x
        self.tracker = 0

    def c(self):
        return self.items[self.current]

    def update_pos(self, y):
        self.y = y + 1

        for i in self.items:
            i.y = self.y

    def update_end(self, x):
        self.cursor = x

    def update_tracker(self, num):
        self.tracker = num + len(self.items)
        return self.tracker

    def add_item(self):
        self.current += 1
        self.items.insert(self.current, Item(self.y, self.cursor))

    def remove_item(self, num):
        del self.items[num]

    def remove_current_item(self):
        if self.current > 0:
            del self.items[self.current]


class Screen:
    def __init__(self):
        self.lines = [Line(start_y)]
        self.current = 0
        self.line = None
        self.item = None
        self.refresh()
        self.header_text = "Isolang Interpreter"

    def update(self, stdscr):
        global digits, start_x, start_y

        height, width = stdscr.getmaxyx()

        self.refresh()
        y = start_y - 1
        tracker = 0
        for l in self.lines:
            l.update_pos(y)
            y += 1
            x = start_x -1

            stdscr.addstr(y, 0, "{:0{}}".format(tracker, digits), curses.A_REVERSE)

            tracker = l.update_tracker(tracker)

            # stdscr.addstr(5, 2, str(tracker) + " " + str(digits))

            for i in l.items:
                i.update_pos(x)
                x = i.end
                if i == self.item:
                    stdscr.attron(curses.A_REVERSE)
                    i.render(stdscr)
                    stdscr.attroff(curses.A_REVERSE)
                else:
                    i.render(stdscr)

            l.update_end(x)

        front_end = math.floor(width / 2 - len(self.header_text) / 2)
        back_end = math.ceil(width / 2 - len(self.header_text) / 2)

        header_text = front_end * " " + self.header_text + back_end * " "
        stdscr.addstr(0, 0, header_text, curses.A_REVERSE)

        # stdscr.addstr(height - 1, 0, (width - 1) * " ", curses.A_REVERSE)

        if tracker >= 10 and digits < 2:  # spacing for item numbers up to 999
            digits += 1
            start_x += 1
        elif tracker < 10 and digits >= 2:
            digits -= 1
            start_x -= 1
        elif tracker >= 100 and digits < 3:
            digits += 1
            start_x += 1
        elif tracker < 100 and digits >= 3:
            digits -= 1
            start_x -= 1

    def refresh(self):
        self.line = self.lines[self.current]
        self.item = self.line.c()

    def add_line(self):
        self.lines.append(Line(start_y + len(self.lines)))
        self.current += 1

    def move_left(self):
        if self.line.current == 0:
            if self.current > 0:
                self.current -= 1
                self.line = self.lines[self.current]
                self.line.current = len(self.line.items) - 1
                self.item = self.line.c()
        else:
            self.line.current -= 1

    def move_right(self):
        if self.line.current == len(self.line.items) - 1:
            if self.current < len(self.lines) - 1:
                self.current += 1
                self.line = self.lines[self.current]
                self.line.current = 0
                self.item = self.line.c()
        else:
            self.line.current += 1

    def move_up(self):
        temp_x = self.line.current
        if self.current != 0:
            self.current -= 1
        self.line = self.lines[self.current]
        self.line.current = min(len(self.line.items) - 1, temp_x)
        self.item = self.line.c()

    def move_down(self):
        temp_x = self.line.current
        if self.current != len(self.lines) - 1:
            self.current += 1
        self.line = self.lines[self.current]
        self.line.current = min(len(self.line.items) - 1, temp_x)
        self.item = self.line.c()

    def backspace(self):
        if self.item.text == "":
            self.line.remove_current_item()
            if self.current > 0:
                if self.line.current == 0:
                    del self.lines[self.current]
            self.move_left()
        else:
            self.item.text = self.item.text[:-1]

    def get_string(self):
        s = ""
        for l in self.lines:
            for w in l.items:
                s += w.text + " "
        return s


start_x = 2
start_y = 1
digits = 1

s = Screen()


def main(stdscr):
    key = 0
    stdscr.clear()
    stdscr.refresh()

    curses.initscr()
    curses.curs_set(0)

    running = True

    global s
    editing = True

    global inter

    inter = interpreter.Interpreter()

    while running:
        stdscr.clear()

        if editing:
            if chr(key) == " ":
                s.line.add_item()
            elif chr(key) == "\n":
                s.add_line()
            elif key == curses.KEY_BACKSPACE:
                s.backspace()
            elif key == curses.KEY_LEFT:
                s.move_left()
            elif key == curses.KEY_RIGHT:
                s.move_right()
            elif key == curses.KEY_UP:
                s.move_up()
            elif key == curses.KEY_DOWN:
                s.move_down()
            elif key == curses.KEY_F1:
                editing = False
                inter.load(s.get_string())
            elif chr(key) in string.printable:
                s.item.text += chr(key)
            s.update(stdscr)
        else:
            editing = True
            running = False
            break

        stdscr.refresh()
        key = stdscr.getch()




while True:
    curses.wrapper(main)
    inter.loop()
    input()
