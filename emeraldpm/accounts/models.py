from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _('A user with that email already exists.'),
        })

    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=150)

    github_username = models.CharField(_('github username'), max_length=39)
    twitter_username = models.CharField(_('twitter username'), max_length=15)
