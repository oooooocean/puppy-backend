from django.contrib import admin

from .models.user import user, user_info
from .models.post import topic

models = [user.User, user_info.UserInfo, topic.PostTopic]

admin.site.site_header = '宠物星球'
for model in models:
    admin.site.register(model)

