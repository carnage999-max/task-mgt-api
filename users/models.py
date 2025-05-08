from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True, error_messages={
        "unique": _("A user with that email already exists")
    })
    username = None
    groups = models.ManyToManyField(Group, verbose_name=_("groups"), blank=True, related_name="user_groups", related_query_name="user")
    user_permissions = models.ManyToManyField(Permission, verbose_name=_("user permissions"), related_name="user_user_permissions", related_query_name="user")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email
    
