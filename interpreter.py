import commands


class Interpreter:
    def __init__(self, file):
        self.priority = 0  # current priority level
        self.current = 0  # current packet

        self.stream = []
        self.load(file)
        # print(self.stream)
        self.var = {}
        self.cmds = []  # highest priority command receives arguments

        self.list_cmd = open("cmd_list.txt", "r").read().split()  # list of all commands
        self.holder = None  # holds returned values until the next command activates
        self.resolve = True
        self.halt = False

    def load(self, file):
        load_stream = []
        with open(file, "r") as f:  # opens file
            text = f.read()
            for w in text.split():  # iterates through all words in text
                if w.isdigit():  # if string is a valid int, converted
                    load_stream.append(int(w))
                else:  # otherwise kept the same
                    load_stream.append(w)
        self.stream = load_stream

    def step(self):

        packet = self.stream[self.current]  # packet is the current item in the stream
        self.current += 1
        packtype = self.get_type(packet)  # packets can be values or commands

        if self.priority:  # if there is a priority
            active = self.cmds[self.priority - 1]  # command with that priority set to active
        else:
            active = None

        if packtype == "cmd":
            self.priority += 1  # new command gets 1 higher priority
            self.cmds.append(self.get_cmd(packet)(self.priority))  # adds new active command

        elif packtype == "val":
            active.argument(packet)  # sends argument to priority command

        while self.resolve:
            active = self.cmds[self.priority - 1]
            self.resolve = False

            if self.holder:
                active.argument(self.holder)
                self.holder = None

            if active.complete():  # on command completion
                type = active.return_type  # get return type
                # passes in requested data to modify
                if type == "var":  # changing var stream
                    self.var = active.evaluate(self.var)
                elif type == "stream":  # changing packet stream
                    self.stream = active.evaluate(self.stream)
                elif type == "current":  # changing current packet
                    self.current = active.evaluate(self.current)
                elif type == "value":  # returns argument for next command
                    self.holder = active.evaluate(self.var)
                    self.resolve = True
                elif type == "none":
                    active.evaluate()
                else:  # error if return type not there or doesn't match
                    self.raise_error(f"'{active.__class__.__name__}' has an invalid return type: '{active.return_type}'")

                del self.cmds[self.priority - 1]  # remove command from active
                self.priority -= 1  # drop priority
            # print("repeat")
        self.resolve = True

        if self.current == len(self.stream):  # stops on last command
            self.halt = True

        # print(self.current, self.var, self.holder)
        # print(self.current, self.priority, active.__class__.__name__, active.args)
        # print(self.priority)


    def loop(self):
        while not self.halt:
            self.step()

    def get_type(self, packet):  # evaluates whether a packet is a command or value
        if type(packet) == int:  # all integers are values
            return "val"
        else:
            if packet in self.list_cmd:  # strings in command list are commands
                return "cmd"
            else:  # if they aren't commands they are string values
                return "val"

    def get_cmd(self, packet):
        if packet == "set":
            return commands.Set
        elif packet == "get":
            return commands.Get
        elif packet == "print":
            return commands.Print
        elif packet == "goto":
            return commands.Goto
        elif packet == "add":
            return commands.Add
        else:
            self.raise_error(f"{packet} is an invalid command")

    def raise_error(self, error):
        print("Error: " + error)
        self.halt = True


interpreter = Interpreter("commands.txt")
# interpreter.load(stream, var)

interpreter.loop()
