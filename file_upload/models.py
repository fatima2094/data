from django.db import models
import os
import uuid
from django.contrib.auth.models import User
from model_utils import Choices

# Create your models here.
# Define user directory path

class active(models.Model):
    user_name = models.CharField(max_length=255)
    
def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return os.path.join("files", filename)


class File(models.Model):
    file = models.FileField(upload_to=user_directory_path) 
    name = models.CharField(max_length=20, verbose_name="filename")
    sec_key = models.CharField(max_length=200)
    allow = models.ManyToManyField(User ,null=True)

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)
