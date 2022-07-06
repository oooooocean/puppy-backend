from enum import IntEnum
from .dog import DogCategory
from .cat import CatCategory


class PetCategory(IntEnum):
    DOG = 0
    CAT = 1

    def __str__(self):
        match self:
            case PetCategory.DOG:
                return '狗狗'
            case PetCategory.CAT:
                return '猫咪'

    @property
    def sub_category(self):
        """
        子类
        """
        match self:
            case PetCategory.DOG:
                return DogCategory
            case PetCategory.CAT:
                return CatCategory

    @property
    def hot_category(self) -> list:
        """
        热门分类
        """
        match self:
            case PetCategory.DOG:
                return [DogCategory.GOLDEN, DogCategory.LABRADOR, DogCategory.BORDER_COLLIE, DogCategory.SATSUMA]
            case PetCategory.CAT:
                return [CatCategory.SNOWSHOE]

    def to_dict(self) -> dict:
        """
        转字典给前端使用
        """
        return {
            'id': self.value,
            'name': str(self),
            'sub_category': [i.to_dict() for i in self.sub_category],
            'hot_category': [i.value for i in self.hot_category]
        }

