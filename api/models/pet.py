from django.db import models
from api.models.pet_category import PetCategory
from api.models.user import User, UserInfo
from api.models.gender import Gender


class Pet(models.Model):
    """
    宠物
    """
    nickname = models.CharField('昵称', max_length=50)
    avatar = models.CharField('照片', max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pets')

    def __str__(self):
        return f'{self.owner.info.nickname}的{self.nickname}'

    @property
    def owner_info(self):
        return UserInfo.objects.get(pk=self.owner.pk)


class PetIntrinsic(models.Model):
    """
    宠物的自然属性
    """
    owner = models.OneToOneField(Pet, on_delete=models.CASCADE, related_name='intrinsic', primary_key=True)
    gender = models.IntegerField('性别', choices=[(i.value, str(i)) for i in Gender])
    category = models.IntegerField('类别', choices=[(i.value, str(i)) for i in PetCategory])
    birthday = models.DateField('生日')
    neuter = models.BooleanField('是否绝育', null=True)

    sub_category = models.IntegerField('子类别')

