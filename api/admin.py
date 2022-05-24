from django.contrib import admin

from .models import user
from .models import pet

models = [user.User, user.UserInfo, pet.Pet]

for model in models:
    admin.site.register(model)

