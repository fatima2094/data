from django.contrib import admin 
from .models import File ,active

# Register your models here.
admin.site.register(active)
admin.site.register(File)