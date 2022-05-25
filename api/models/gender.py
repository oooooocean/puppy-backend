from enum import IntEnum


class Gender(IntEnum):
    """
    性别
    """
    MALE = 0
    FEMALE = 1

    def __str__(self):
        return '男' if self == Gender.MALE else '女'
