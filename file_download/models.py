from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Downkey(models.Model):
    #owner = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)

    sec_key = models.CharField(max_length=100)
  