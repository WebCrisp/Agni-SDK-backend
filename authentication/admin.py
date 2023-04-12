from django.contrib import admin
from .models import UserProfile, Projects

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Projects)