from django.urls import path, include
from rest_framework.routers import SimpleRouter
from api.views import (
    pet,
    user,
    user_info
)
import api.common.configuration as configuration

app_name = 'api'

router = SimpleRouter()
router.register('user', user.UserViewSet, basename='user')  # 用户

pet_router = SimpleRouter()
pet_router.register('pets', pet.PetViewSet, basename='pet')  # 宠物

configuration_urlpatterns = [
    path('app/', configuration.get_app_configuration),
    path('pet/', configuration.get_pet_category)
]

urlpatterns = [
    path('configuration/', include(configuration_urlpatterns)),
    path('user/<int:user_id>/info/',
         user_info.UserInfoViewSet.as_view({'get': 'retrieve', 'patch': 'update', 'post': 'create'})),
    path('', include(router.urls)),
    path('user/<int:user_id>/', include(pet_router.urls))
]
