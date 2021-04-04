from enum import Enum

# Варианты типа чека
class CheckTypes(Enum):
    kitchen = ('k', 'Kitchen')
    client = ('c', 'Client')

    # @classmethod
    # def choices(types):
    #     return [(key.value[-1], key.name) for key in types]
    @classmethod
    def choices(types):
        return [type.value for type in types]
