from enum import IntEnum


class DogCategory(IntEnum):
    """
    https://baijiahao.baidu.com/s?id=1719496020058996183&wfr=spider&for=pc
    """
    GOLDEN = 0
    SATSUMA = 1
    BORDER_COLLIE = 2
    POODLE = 3
    GERMAN_SHEPHERD_DOG = 4
    DOBERMAN = 5
    SHETLAND = 6
    LABRADOR = 7
    PAPILLON = 8
    ROTTWEILER = 9
    BLUEHEELER = 10

    def __str__(self):
        return ['金毛寻回猎犬', '萨摩耶犬', '边境牧羊犬', '贵宾犬',
                '德国牧羊犬', '杜宾犬', '喜乐蒂牧羊犬', '拉布拉多猎犬',
                '蝴蝶犬', '罗威纳犬', '澳洲牧牛犬'][self.value]

    @property
    def image(self):
        return f'dog/{self.name}.jpeg'

    def to_dict(self):
        return {'id': self.value, 'name': str(self), 'image': self.image}
