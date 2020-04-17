from django.contrib import admin
from . import models
from .models import UserProfileInfo, User

# Register your models here.
admin.site.register(models.Task)
admin.site.register(UserProfileInfo)