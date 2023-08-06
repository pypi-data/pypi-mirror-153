from enum import Enum


class SymbiontFunctionType(Enum):
    clientside = 1
    executable = 2
    public = 3

    def __str__(self):
        return self.name
