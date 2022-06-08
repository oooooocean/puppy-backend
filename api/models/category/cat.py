from enum import IntEnum


class CatCategory(IntEnum):
    """
    https://www.bagong.cn/cat/
    """
    SNOWSHOE = 0
    SIAMESE = 1
    SINGAPORE = 2
    HIMALAYA = 3

    def __str__(self):
        return ['雪鞋猫', '暹罗猫', '新加坡猫', '喜玛拉雅猫'][self.value]

    @property
    def image(self):
        return f'cat/{self.name}.jpeg'

    def to_dict(self):
        return {'id': self.value, 'name': str(self), 'image': self.image}
