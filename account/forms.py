from . import models
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    class Meta:
        model = models.User
        exclude = ['is_staff', 'is_active', 'is_superuser', 'date_joined', 'last_login',
                   'groups', 'user_permissions', 'avatar', 'address', 'password']
