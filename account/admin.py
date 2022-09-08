from django.contrib import admin
from . import models
class UserAdmin(admin.ModelAdmin):
    ...


admin.site.register(models.User, UserAdmin)
