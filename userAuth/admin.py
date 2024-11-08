from django.contrib import admin
from .models import User, Profile

class ConfUser(admin.ModelAdmin):
    list_display = ['id', 'username', 'email']

class ConfProfile(admin.ModelAdmin):
    list_display = ['user_id', 'user', 'full_name', 'date']

admin.site.register(User, ConfUser)
admin.site.register(Profile, ConfProfile)
