from enum import IntEnum
from api.models.category.dog import DogCategory
from api.models.support import IdAndName


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
        """
        子类
        """
        match self:
            case PetCategory.DOG:
                return [IdAndName(dog.value, str(dog))._asdict() for dog in DogCategory]
            case PetCategory.CAT:
                return []

    def to_dict(self) -> dict:
        """
        转字典给前端使用
        """
        return {
            'id': self.value,
            'name': str(self),
            'sub_category': self.sub_category()
        }

