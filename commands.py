class Command:
    def __init__(self, interpreter, max_args):
        self.num_args = 0  # number of arguments currently stored
        self.max_args = max_args  # maximum arguments (if applicable)

        if max_args == 0:  # determine if command accept args
            self.accept_args = False
        else:
            self.accept_args = True

        self.args = []  # list of actual arguments of a function
        self.flag = False  # flag turned on every time an arg is added
        self.completed = False  # command removed from stack if completed

        self.inter = interpreter  # pointer to interpreter object stored in commands

    def argument(self, arg):
        if self.accept_args:
            self.args.append(arg)  # add arg
            self.num_args += 1
            self.flag = True  # flags an arg has been added
        else:
            self.inter.raise_error(f"{self.__class__.__name__} command does not accept arguments")

    def last(self):  # handles the last action a command takes
        if self.num_args == self.max_args:  # if all arguments filled
            self.completed = True
            return True
        else:
            return False


class Set(Command):  # sets variable value in var stream
    def __init__(self, inter):
        super().__init__(inter, 2)

    def execute(self):
        if self.last():
            self.inter.var[self.args[0]] = self.args[1]


class Get(Command):  # gets variable value from var stream
    def __init__(self, inter):
        super().__init__(inter, 1)

    def execute(self):
        if self.last():
            return self.inter.var[self.args[0]]  # returns arg value from var dict


class Print(Command):
    def __init__(self, inter):
        super().__init__(inter, 1)

    def execute(self):
        if self.last():
            print(self.args[0])


class Goto(Command):
    def __init__(self, inter):
        super().__init__(inter, 1)

    def execute(self):
        if self.last():
            self.inter.current = self.args[0]


class Add(Command):
    def __init__(self, inter):
        super().__init__(inter, 2)

    def execute(self):
        if self.last():
            return self.args[0] + self.args[1]


class Sub(Command):
    def __init__(self, inter):
        super().__init__(inter, 2)

    def execute(self):
        if self.last():
            return self.args[0] - self.args[1]


class Mult(Command):
    def __init__(self, inter):
        super().__init__(inter, 2)

    def execute(self):
        if self.last():
            return round(self.args[0] * self.args[1])


class Div(Command):
    def __init__(self, inter):
        super().__init__(inter, 2)

    def execute(self):
        if self.last():
            return round(self.args[0] / self.args[1])


class Less(Command):
    def __init__(self, inter):
        super().__init__(inter, 2)

    def execute(self):
        if self.last():
            return self.args[0] < self.args[1]


class More(Command):
    def __init__(self, inter):
        super().__init__(inter, 2)

    def execute(self):
        if self.last():
            return self.args[0] > self.args[1]


class If(Command):
    def __init__(self, inter):
        super().__init__(inter, -1)
        self.conditional = None

    def execute(self):
        if self.num_args == 1:
            if self.args[0] <= 0:  # conditional evaluates to false (x <= 0)
                if not self.next("else"):  # goto next else
                    if not self.next("end"):  # if none found goto next end
                        self.inter.raise_error(f"if statement does not end")
                self.conditional = False
            else:  # conditional evaluates to true (x > 0)
                self.conditional = True

        elif self.num_args == 2:  # second arg ends or continues if command
            if self.args[1] == 0:  # "end" ends if statement
                self.completed = True
            elif self.args[1] == 1:  # "else" continues if statement
                if self.conditional:  # if conditional is true, skip over else command
                    if not self.next("end"):  # goto next end
                        self.inter.raise_error(f"if statement does not end")

        elif self.num_args == 3:
            if self.args[2] == 0:
                self.completed = True

    def next(self, cmd):  # searches for a given command ahead
        forward = self.inter.stream[self.inter.current:]  # forward stream from current position
        endpoint = 0
        for c, item in enumerate(forward):  # find first occurrence of end command
            if item == cmd:
                endpoint = c  # save end position
                break
        self.inter.current += endpoint  # jump to end position
        if endpoint == 0:  # returns whether it successfully found the command
            return False
        else:
            return True


class End(Command):
    def __init__(self, inter):
        super().__init__(inter, 0)

    def execute(self):
        self.completed = True
        return 0


class Else(Command):
    def __init__(self, inter):
        super().__init__(inter, 0)

    def execute(self):
        self.completed = True
        return 1


class Input(Command):
    def __init__(self, inter):
        super().__init__(inter, 0)

    def execute(self):
        self.completed = True
        i = input()

        try:  # determines if item is a integer
            i = int(i)
        except ValueError:
            pass

        return i


class Dummy(Command):
    def __init__(self, inter):
        super().__init__(inter, 0)

    def execute(self):
        pass


class Example(Command):  # example command
    def __init__(self, inter):
        super().__init__(inter, 0)  # number of args passed in

    def execute(self):  # modify interpreter values with inter
        pass  # returned values are passed to the next active command
