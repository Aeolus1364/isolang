class Command:
    def __init__(self, num_args):
        self.num_args = num_args  # number of arguments it takes
        self.args = []  # list of actual arguments of a function
        self.active = True

    def argument(self, arg):
        self.args.append(arg)
        self.num_args -= 1

    def complete(self):
        if self.num_args < 0:
            print("Error: number of arguments less than zero")
        return self.num_args == 0


class Set(Command):  # sets variable value in var stream
    def __init__(self):
        super().__init__(2)
        # arg 0: var name
        # arg 1: var value

    def evaluate(self, inter):
        inter.var[self.args[0]] = self.args[1]


class Get(Command):  # gets variable value from var stream
    def __init__(self):
        super().__init__(1)
        # arg 0: var name

    def evaluate(self, inter):
        return inter.var[self.args[0]]  # returns arg value from var dict


class Print(Command):
    def __init__(self):
        super().__init__(1)
        # arg 0: prints value

    def evaluate(self, inter):
        print(self.args[0])


class Goto(Command):
    def __init__(self):
        super().__init__(1)

    def evaluate(self, inter):
        inter.current = self.args[0]


class Add(Command):
    def __init__(self):
        super().__init__(2)

    def evaluate(self):
        return self.args[0] + self.args[1]


class Example(Command):  # example command
    def __init__(self):
        super().__init__(0)  # number of args passed in

    def evaluate(self, inter):  # modify interpreter values with inter
        pass  # returned values are passed to the next active command
