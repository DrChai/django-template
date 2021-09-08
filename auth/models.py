from auth_framework.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    settings = models.JSONField(_('account settings'), default=dict)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
