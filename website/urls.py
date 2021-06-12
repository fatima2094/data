from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import  LogoutView
from users.views import LoginUser
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls', namespace='users')),
    path('profile/', include('profiles.urls', namespace='profiles')),
    path('file/', include("file_upload.urls")),
    path('file/', include("file_download.urls")),
]

urlpatterns += [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
 
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


