from django.contrib import admin
from . import models


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.User, UserAdmin)
