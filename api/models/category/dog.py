from enum import IntEnum


class DogCategory(IntEnum):
    GOLDEN = 0
    SATSUMA = 1

    def __str__(self):
        match self:
            case DogCategory.GOLDEN:
                return '金毛'
            case DogCategory.SATSUMA:
                return '萨摩耶'

