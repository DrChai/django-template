from django.contrib.auth import get_user_model
from django.contrib import admin
from auth_framework.admin import UserAdmin
# Register your models here.
User = get_user_model()
admin.site.register(User, UserAdmin)