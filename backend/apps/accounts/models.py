from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.db.models import Q
from django.conf import settings

from apps.crossuser.models import UserId


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        email = self.normalize_email(email)

        user, created = self.model.objects.using(settings.USERS_DB).get_or_create(username=username, email=email, **extra_fields)
        if created:
            user.set_password(password)
            user.save(using=settings.USERS_DB)
        
        # user_id = UserId(id_user=user.id)
        # user_id.save(using=self._db)
        UserId.objects.using(self._db).get_or_create(id_user=user.id)
        
        # user = self.model(username=username, email=email, **extra_fields)
        # user.set_password(password)
        # user.save(using="users")
        # user_id = UserId(id_user=user.id)
        # user_id.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        user = self.create_user(username, email, password=password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=settings.USERS_DB)
        UserId.objects.using(self._db).get_or_create(id_user=user.id)
        return user

    def get_by_natural_key(self, username):
        return self.get(
            Q(**{self.model.USERNAME_FIELD: username}) |
            Q(**{self.model.EMAIL_FIELD: username})
        )


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=False)
    full_name = models.CharField(max_length=255, verbose_name="Full name", blank=True, null=True)
    is_active = models.BooleanField(default=False, verbose_name="Active")
    is_staff = models.BooleanField(default=False, verbose_name="Staff permissions")
    is_admin = models.BooleanField(default=False, verbose_name="Superuser permissions")

    objects = UserManager()

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.username