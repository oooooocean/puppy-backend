from enum import Enum
from configparser import ConfigParser
from rest_framework import decorators
from api.models.category.pet import PetCategory
from api.common.responses import success_response

config = ConfigParser()
config.read('api/common/configuration.ini')


class Configuration(Enum):
    """
    获取指定的配置
    """
    MAX_PET_COUNT = 'app-max_pet_count'  # 最大宠物数量
    MAX_INTRODUCTION = 'app-max_introduction'  # 个性签名最大字数限制

    @property
    def evaluation(self):
        group, key = self.value.split('-')
        return config.get(group, key)


@decorators.api_view()
def get_app_configuration(_):
    """
    app 配置
    """
    return success_response({k: v for k, v in config.items('app')})


@decorators.api_view()
def get_pet_category(_):
    """
    宠物分类
    """
    return success_response([i.to_dict() for i in PetCategory])
