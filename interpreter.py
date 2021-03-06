import commands
import time


class Interpreter:
    def __init__(self):
        self.current = 0

        self.stream = []  # stream of packets
        self.var = {}
        self.stack = []  # commands in effect, most recent is active

        self.halt = False
        self.resolved = False

        self.item = None
        self.active = None
        self.type = None
        self.holder = None

    def load(self, text):  # load code from string
        load_stream = []
        for w in text.split():  # iterates through all words in text
            try:  # determines if item is a integer
                int(w)
                is_int = True
            except ValueError:
                is_int = False
            if is_int:  # if string is a valid int, converted
                load_stream.append(int(w))
            else:  # otherwise kept the same
                load_stream.append(w)
        self.stream = load_stream

    def load_file(self, file):  # load code from file
        load_stream = []
        with open(file, "r") as f:  # opens file
            text = f.read()
            for w in text.split():  # iterates through all words in text
                try:  # determines if item is a integer
                    int(w)
                    is_int = True
                except ValueError:
                    is_int = False
                if is_int:  # if string is a valid int, converted
                    load_stream.append(int(w))
                else:  # otherwise kept the same
                    load_stream.append(w)
        self.stream = load_stream

    def step(self):
        if self.stream:  # if there is code
            self.item = self.stream[self.current]
            self.current += 1

            # determines item type: cmd or val
            if type(self.item) == int:  # all integers all values
                self.type = "val"
            elif self.item[0] == '.':  # . value classifier for non command strings
                self.type = "val"
                self.item = self.item[1:]  # removing . value classifier
            else:
                self.type = "cmd"

            # action taken based on item type
            if self.type == "cmd":
                try:
                    self.stack.append(  # adds command to stack
                        getattr(commands, self.item.capitalize())(self)  # command class fetched from string
                    )
                except AttributeError:
                    self.raise_error(f"{self.item.capitalize()} is not a command")

            elif self.type == "val":
                if self.stack:  # if there is an active command
                    self.active.argument(self.item)  # value passed into active command
                else:  # skip command resolution if stack is empty
                    self.resolved = True

            # resolves all completable commands
            while not self.resolved:
                self.active = self.stack[-1]  # active command is the top of the stack

                if self.holder is not None:  # if the holder contains a value
                    self.active.argument(self.holder)  # pass in holder as an argument
                    self.holder = None  # reset holder to None

                self.holder = self.active.execute()  # evaluate the command and hold any returned value

                if self.active.completed:  # is command completed?
                    del self.stack[-1]  # remove completed command from the stack

                if self.holder is None:
                    self.resolved = True  # all actions are resolved, end step

                # print(self.active.__class__.__name__, self.active.args, self.holder)

            # print(self.current, self.item, self.var)
            # print(self.active.__class__.__name__, self.active.args, self.stack)
            # print()

            self.resolved = False

            if self.current == len(self.stream):  # if last item is reached, end program
                self.halt = True

    def loop(self):
        while not self.halt:
            self.step()
            time.sleep(0.01)

    def raise_error(self, error):
        print("Error: " + error)
        self.halt = True

# i = Interpreter()
# i.load_file("code.txt")
# i.loop()