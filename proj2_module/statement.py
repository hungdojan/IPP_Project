import sys
from .error import ErrorCode
from .coredata import CoreData

class Argument:

    def __init__(self, arg):
        self.type = arg[0]
        if self.type in ('var', 'string', 'label', 'type'):
            self.value = arg[1]
        elif self.type == 'bool':
            self.value = arg[1] == 'true'
        elif self.type == 'int':
            self.value = int(arg[1])
        elif self.type == 'float':
            pass # TODO: float
        else:   # nil type
            self.value = None


    def __str__(self):
        return f"\ntype: {self.type}, value: {self.value}"

    def __repr__(self):
        return str(self)


class Statement:

    def __init__(self, ins, order: int, args: list):
        self.ins   = ins.upper()
        self.order = order
        self.args  = [Argument(arg) for arg in args]

        if ins == 'LABEL':
            label_name = self.args[0].value
            if CoreData.labels.get(label_name) is not None:
                sys.exit(ErrorCode.SEMANTIC_ERROR)
            CoreData.labels[label_name] = order


    def __str__(self):
        return f"{self.ins}, {self.order}, {self.args}"


    def __repr__(self):
        return str(self)
