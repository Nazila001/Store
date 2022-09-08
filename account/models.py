from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid
import os


def _get_avatar_upload_path(obj, filename):
    now = timezone.now()
    base_path = "avatars"
    new_filename = str(uuid.uuid5(uuid.NAMESPACE_URL, obj.pk))
    ext = os.path.splitext(filename)[1]
    p = os.path.join(base_path, now.strftime("%Y/%m"), f"{new_filename}{ext}")
    return p


class User(AbstractUser):
    email = models.EmailField('Email address', blank=False)
    phone = models.CharField('Phone number', max_length=15)
    address = models.TextField('Address', max_length=255, blank=True, null=True)
    avatar = models.ImageField(upload_to=_get_avatar_upload_path, blank=True, null=True)

    def __str__(self):
        return f"{self.username}"
