from enum import Enum

# Варианты типа чека
class CheckTypes(Enum):
    kitchen = ('k', 'Kitchen')
    client = ('c', 'Client')

    @classmethod
    def choices(types):
        return [type.value for type in types]

# Варианты статуса чека
class CheckStatus(Enum):
    new = ('n', 'New')
    rendered = ('r', 'Rendered')
    printed = ('p', 'Printed')

    @classmethod
    def choices(types):
        return [type.value for type in types]
