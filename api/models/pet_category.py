from enum import IntEnum
from api.models.dog_category import DogCategory
from collections import namedtuple

Animal = namedtuple('Animal', ['id', 'name'])


class PetCategory(IntEnum):
    DOG = 0
    CAT = 1

    def __str__(self):
        match self:
            case PetCategory.DOG:
                return '狗狗'
            case PetCategory.CAT:
                return '猫咪'

    def sub_category(self) -> list:
        match self:
            case PetCategory.DOG:
                return [Animal(dog.value, str(dog)) for dog in DogCategory]
            case PetCategory.CAT:
                return []
