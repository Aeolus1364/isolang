class Command:
    def __init__(self, interpreter, max_args):
        self.num_args = 0  # number of arguments it takes
        self.max_args = max_args
        if max_args == 0:
            self.accept_args = False
        else:
            self.accept_args = True
        self.args = []  # list of actual arguments of a function
        self.flag = False  # flag turned on every time an arg is added
        self.completed = False  # command removed from stack if completed

        self.inter = interpreter

    def argument(self, arg):
        if self.accept_args:
            self.args.append(arg)
            self.num_args += 1
            self.flag = True
        else:
            print(f"Error: {self.__class__.__name__} command does not accept arguments")


class Set(Command):  # sets variable value in var stream
    def __init__(self, inter):
        super().__init__(inter, 2)

    def execute(self):
        if self.num_args == self.max_args:
            self.inter.var[self.args[0]] = self.args[1]
            self.completed = True


class Get(Command):  # gets variable value from var stream
    def __init__(self, inter):
        super().__init__(inter, 1)

    def execute(self):
        if self.num_args == self.max_args:
            self.completed = True
            return self.inter.var[self.args[0]]  # returns arg value from var dict


class Print(Command):
    def __init__(self, inter):
        super().__init__(inter, 1)
        # arg 0: prints value

    def execute(self):
        if self.max_args == self.num_args:
            self.completed = True

            print(self.args[0])
#
#
# class Goto(Command):
#     def __init__(self):
#         super().__init__(1)
#
#     def evaluate(self, inter):
#         inter.current = self.args[0]
#
#
# class Add(Command):
#     def __init__(self):
#         super().__init__(2)
#
#     def evaluate(self, inter):
#         return self.args[0] + self.args[1]
#
#
# class If(Command):
#     def __init__(self):
#         super().__init__(2)
#
#     def evaluate(self, inter):
#         if (self.args[0] < 0):
#             for c in range(inter.current, len(inter.stream)):
#                 if c == "end"
#
                
class End(Command):
    def __init__(self):
        super().__init__(0)
        
    def evaluate(self):
        return 1            
          
        
class Dummy(Command):
    def __init__(self):
        super().__init__(0)
        
    def evaluate(self):
        pass
    
    
class Example(Command):  # example command
    def __init__(self):
        super().__init__(0)  # number of args passed in

    def evaluate(self, inter):  # modify interpreter values with inter
        pass  # returned values are passed to the next active command
