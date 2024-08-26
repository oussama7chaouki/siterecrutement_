from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    avatar = models.ImageField(null=True, default="avatar-01.jpg")
    role = models.IntegerField(null=True, default=2)
    status = models.IntegerField(default=1)
    activation = models.IntegerField(default=1)

    REQUIRED_FIELDS = []
