import re
import sys
from .error import ErrorCode
from .coredata import CoreData

class Statement:

    class Argument:

        def __init__(self, arg):
            self.type = arg[0]
            if self.type == 'string':
                self._format_string(arg[1])
            elif self.type in ('var', 'label', 'type'):
                self.value = arg[1]
            elif self.type == 'bool':
                self.value = arg[1] == 'true'
            elif self.type == 'int':
                self.value = int(arg[1])
            elif self.type == 'float':
                self.value = float.fromhex(arg[1])
            else:   # nil type
                self.value = None

        def _format_string(self, str_val: str):
            """ Format string into printable value """

            def ascii_to_str(match_obj):
                """ Convert \XXX format into ascii_char_value """
                ascii_value = int(match_obj.group(0)[1:])
                return chr(ascii_value)

            if str_val is None:
                self.value = ''
            else:
                self.value = re.sub(r'\\\d{3}', ascii_to_str, str_val)

        def __str__(self):
            return f"\ntype: {self.type}, value: {self.value}"

        def __repr__(self):
            return str(self)

    def __init__(self, ins, order: int, args: list):
        self.ins   = ins
        self.order = order
        self.args  = [self.Argument(arg) for arg in args]

        if ins == 'LABEL':
            label_name = self.args[0].value
            if CoreData.labels.get(label_name) is not None:
                sys.exit(ErrorCode.SEMANTIC_ERROR)
            CoreData.labels[label_name] = 0

            # remove from undefined label if exists
            if label_name in CoreData.undef_labels:
                CoreData.undef_labels.remove(label_name)

        elif ins in ('JUMP', 'JUMPIFEQ', 'JUMPIFNEQ', 'CALL'):
            # add label to undefined label if label doesn't exists yet
            if CoreData.labels.get(self.args[0].value) is None:
                CoreData.undef_labels.append(self.args[0].value)


    def __str__(self):
        return f"{self.ins}, {self.order}, {self.args}"


    def __repr__(self):
        return str(self)
