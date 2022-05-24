from auth_framework.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    settings = models.JSONField(_('account settings'), default=dict)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    @classmethod
    def get_fields(cls):
        # strip out private fields for DRF serializers
        return tuple(set(map(lambda field: field.name, cls._meta.local_fields)) -
                     {'password', 'is_superuser', 'is_active', 'last_login', 'is_staff', 'date_joined'})
