from django.contrib import admin
from .models import code

from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile


# Register your models here.

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserProfileAdmin(UserAdmin):
    inlines = (UserProfileInline,)


admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserProfileAdmin)

admin.site.register(UserProfile)    
admin.site.register(code)
