from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth import get_user_model



class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_field):
        if not email:
            raise ValueError("Using email!")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_field)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_field):
        extra_field.setdefault("is_staff", False)
        extra_field.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_field)


    def create_superuser(self, email, password=None, **extra_field):
        extra_field.setdefault("is_staff", True)
        extra_field.setdefault("is_superuser", True)
        if extra_field.get("is_staff") is not True:
            raise ValueError(
            "superuser must have is_staff=True"
        )
        if extra_field.get("is_superuser") is not True:
            raise ValueError(
            "superuser must have is_superuser=True"
        )
        return self._create_user(email, password, **extra_field)
        

class User(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    
    def __str__(self):
        return f"{self.email}"


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField("Content", max_length=150, blank=False, null=False)
    is_complete = models.BooleanField("Is Complete", default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content