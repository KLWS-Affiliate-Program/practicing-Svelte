from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom user model with role-based access control."""

    ROLE_CHOICES = [
        ("viewer", "Viewer"),
        ("rep", "Sales Rep"),
        ("manager", "Manager"),
        ("admin", "Admin"),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="viewer")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email

    @property
    def is_viewer(self):
        return self.role == "viewer"

    @property
    def is_rep(self):
        return self.role == "rep"

    @property
    def is_manager(self):
        return self.role in ["manager", "admin"]

    @property
    def is_admin_role(self):
        return self.role == "admin"


class SystemConfig(models.Model):
    """System-wide configuration - single row table."""

    base_currency = models.CharField(
        max_length=3,
        default="USD",
        help_text="Base currency for all deal values",
    )
    default_timezone = models.CharField(
        max_length=50,
        default="UTC",
        help_text="Default timezone for reports and SLA calculations",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "System Configuration"
        verbose_name_plural = "System Configuration"

    def __str__(self):
        return "System Config"

    @classmethod
    def get_config(cls):
        """Get or create the single system config instance."""
        config, _ = cls.objects.get_or_create(pk=1)
        return config
