from enum import Enum

# Варианты типа чека
class CheckTypes(Enum):
    k = 'kitchen'
    c = 'client'

    @classmethod
    def choices(types):
        return [(key.value[-1], key.name) for key in types]
