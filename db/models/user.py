from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.db import models
from django.conf import settings
import pytz
import uuid
from django.utils import timezone
import random
import string



def get_default_onboarding():
    return {
        'email_verified': False,
        'profile_complete': False,
        'workspace_create': False,
        'workspace_join': False,
    }
    
class User(AbstractBaseUser):
     
    username = models.CharField(max_length=128, unique=True)
    mobile_number = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, null=True,
                             blank=True, unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    avatar = models.CharField(max_length=255, blank=True)
    cover_image = models.URLField(blank=True, null=True, max_length=800)
    password = models.CharField(max_length=128, default='')
    # tracking metrics
    date_joined = models.DateTimeField(
        auto_now_add=True, verbose_name="Created At")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Last Modified At")
    last_location = models.CharField(max_length=255, blank=True)
    created_location = models.CharField(max_length=255, blank=True)
    email_code = models.CharField(max_length=20, default='')
    # the is' es
    is_superuser = models.BooleanField(default=False)
    is_managed = models.BooleanField(default=False)
    is_password_expired = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_password_autoset = models.BooleanField(default=False)
    is_onboarded = models.BooleanField(default=False)

    token = models.CharField(max_length=64, blank=True)

    billing_address_country = models.CharField(max_length=255, default="INDIA")
    billing_address = models.JSONField(null=True)
    has_billing_address = models.BooleanField(default=False)

    USER_TIMEZONE_CHOICES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    user_timezone = models.CharField(
        max_length=255, default="UTC", choices=USER_TIMEZONE_CHOICES)

    last_active = models.DateTimeField(default=timezone.now, null=True)
    last_login_time = models.DateTimeField(null=True)
    last_logout_time = models.DateTimeField(null=True)
    last_login_ip = models.CharField(max_length=255, blank=True)
    last_logout_ip = models.CharField(max_length=255, blank=True)
    last_login_medium = models.CharField(
        max_length=20,
        default="email",
    )
    last_login_uagent = models.TextField(blank=True)
    token_updated_at = models.DateTimeField(null=True)
    last_workspace_id = models.UUIDField(null=True)
    my_issues_prop = models.JSONField(null=True)
    role = models.CharField(max_length=300, null=True, blank=True)
    is_bot = models.BooleanField(default=False)
    theme = models.JSONField(default=dict)
    display_name = models.CharField(max_length=255, default="")
    is_tour_completed = models.BooleanField(default=False)
    onboarding_step = models.JSONField(default=get_default_onboarding)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "users"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.username} <{self.email}>"

    def save(self, *args, **kwargs):
        self.email = self.email.lower().strip()
        self.mobile_number = self.mobile_number

        if self.token_updated_at is not None:
            self.token = uuid.uuid4().hex + uuid.uuid4().hex
            self.token_updated_at = timezone.now()

        if not self.display_name:
            self.display_name = (
                self.email.split("@")[0]
                if len(self.email.split("@"))
                else "".join(random.choice(string.ascii_letters) for _ in range(6))
            )

        if self.is_superuser:
            self.is_staff = True

        super(User, self).save(*args, **kwargs)

class VerificationCode(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
    )
    code = models.CharField(max_length = 20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)