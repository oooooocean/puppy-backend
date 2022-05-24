from enum import IntEnum


class Gender(IntEnum):
    MALE = 0
    FEMALE = 1

    def __str__(self):
        return '男' if self == Gender.MALE else '女'