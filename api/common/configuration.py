from enum import Enum
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
import configparser

config = configparser.ConfigParser()
config.read('api/common/configuration.ini')


@api_view()
def get_app_configuration(request):
    return Response({k: v for k, v in config.items('app')})


class Configuration(Enum):
    MAX_PET_COUNT = 'app-max_pet_count'

    @property
    def evaluation(self):
        group, key = self.value.split('-')
        return config.get(group, key)
