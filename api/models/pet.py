from django.db import models
from api.models.category.pet import PetCategory
from api.models.user import User, UserInfo
from api.models.gender import Gender
from api.common.configuration import Configuration


class Pet(models.Model):
    """
    宠物
    """
    nickname = models.CharField('昵称', max_length=50)
    avatar = models.CharField('照片', max_length=255)
    introduction = models.CharField('个性签名', max_length=int(Configuration.MAX_INTRODUCTION.evaluation), blank=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pets')  # 主人

    def __str__(self):
        return f'{self.owner.info.nickname}的{self.nickname}'


class PetIntrinsic(models.Model):
    """
    宠物的自然属性
    """
    owner = models.OneToOneField(Pet, on_delete=models.CASCADE, related_name='intrinsic', primary_key=True)
    gender = models.IntegerField('性别', choices=[(i.value, str(i)) for i in Gender])
    category = models.IntegerField('类别', choices=[(i.value, str(i)) for i in PetCategory])
    sub_category = models.IntegerField('子类别')
    birthday = models.DateField('生日')
    neuter = models.BooleanField('是否绝育', null=True)

