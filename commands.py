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
            print(f"Error: {self.__class__.__name__} command does not accept arguments")

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
        print(self.num_args, self.args, self.max_args)
        if self.last():
            return self.args[0] + self.args[1]


# class If(Command):
#     def __init__(self, inter):
#         super().__init__(inter, 2)
#
#     def execute(self, inter):
#         if (self.args[0] < 0):
#             for c in range(inter.current, len(inter.stream)):
#                 if c == "end"


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
