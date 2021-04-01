from enum import Enum

class CheckTypes(Enum):
    k = 'kitchen'
    c = 'client'

    @classmethod
    def choices(types):
        return [(key.value[-1], key.name) for key in types]
