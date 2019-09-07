from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, _user_has_perm
)
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class UserManager(BaseUserManager):
    #ゲストユーザーのmanager
    def create_user_guest(self, request_data, **kwargs):
        now = timezone.now()
        if not request_data['email']:
            raise ValueError('Users must have an email address.')

        user = self.model(
            # username=request_data['username'],
            email=self.normalize_email(request_data['email']),
            is_active=True,
            # last_login=now,
            date_joined=now,
            is_host=False,
            
            # profile=profile
        )

        user.set_password(request_data['password'])
        user.save(using=self._db)
        return user
    
    #ホストユーザーのmanager
    def create_user_host(self, request_data, **kwargs):
        now = timezone.now()
        if not request_data['email']:
            raise ValueError('Users must have an email address.')

        user = self.model(
            # username=request_data['username'],
            email=self.normalize_email(request_data['email']),
            is_active=True,
            # last_login=now,
            date_joined=now,
            is_host=True,
            # profile=profile
        )

        user.set_password(request_data['password'])
        user.save(using=self._db)
        return user
    
    # 管理者のmanager(hostではない)
    def create_superuser(self, email, password, **extra_fields):
        request_data = {
            # 'username': username,
            'email': email,
            'password': password
        }
        user = self.create_user_guest(request_data)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        # user.is_superuser = True
        user.save(using=self._db)
        return user

# Userモデル
class User(AbstractBaseUser):
    # username    = models.CharField(_('username'), max_length=30, unique=True)
    # first_name  = models.CharField(_('first name'), max_length=30, blank=True)
    # last_name   = models.CharField(_('last name'), max_length=30, blank=True)
    email       = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    # profile     = models.CharField(_('profile'), max_length=255, blank=True)
    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)
    is_admin    = models.BooleanField(default=False)
    is_host     = models.BooleanField(default=False)
    is_info     = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']

    def user_has_perm(user, perm, obj):
        return _user_has_perm(user, perm, obj)

    def has_perm(self, perm, obj=None):
        return _user_has_perm(self, perm, obj=obj)

    def has_module_perms(self, app_label):
        return self.is_admin

    # def get_short_name(self):
    #     return self.first_name

    @property
    def is_superuser(self):
        return self.is_admin

    class Meta:
        db_table = 'user'
        swappable = 'AUTH_USER_MODEL'


# Guest_infoモデル
class Guest_info(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    country     = models.CharField(max_length=8)
    birth_day   = models.DateField(null=True)
    address     = models.CharField(max_length=255)
    gender      = models.BooleanField(null=True)
    qr_code     = models.CharField(max_length=255, unique=True, null=True)
    
    USERNAME_FIELD = 'user'
    
    class Meta:
        db_table = 'guest_info'
    