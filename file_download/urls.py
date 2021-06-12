from django.urls import path, re_path
from . import views

# namespace
app_name = 'file_download'

urlpatterns = [

    path('ddd', views.add_blog, name='formm'),

    re_path(r'^download/(?P<file_path>.*)/$', views.file_response_download, name='file_download'),


]
