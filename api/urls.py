from django.urls import path, include
from rest_framework.routers import SimpleRouter
from api.views.user import pet, user_info, user
from api.views.post import topic, post, collect
from api.views.social import follow
from api.views.support import feedback
import api.common.configuration as configuration
import thirdparty.qiniu.upload as upload

app_name = 'api'

router = SimpleRouter()
router.register('user', user.UserViewSet, basename='user')  # 用户
router.register('post/topics', topic.PostTopicViewSet, basename='topic')
router.register('post', post.PostViewSet, basename='post')
router.register('follow', follow.FollowViewSet, basename='follow')


pet_router = SimpleRouter()
pet_router.register('pets', pet.PetViewSet, basename='pet')  # 宠物

post_router = SimpleRouter()

urlpatterns = [
    path('configuration/', include([
        path('app/', configuration.get_app_configuration),
        path('pet/', configuration.get_pet_category)
    ])),
    path('', include([
        path('upload_token/', upload.get_upload_tokens),
        path('feedback/', feedback.FeedbackView.as_view())
    ])),
    path('user/<int:user_id>/info/',
         user_info.UserInfoViewSet.as_view({'get': 'retrieve', 'patch': 'update', 'post': 'create'})),  # 不使用自动构建的url
    path('user/<int:user_id>/', include(pet_router.urls)),
    path('', include(router.urls)),
]
