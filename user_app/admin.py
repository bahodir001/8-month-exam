from django.contrib import admin

from .models import UserModel, CartModels
# Register your models here.

admin.site.register(UserModel)
admin.site.register(CartModels)