from django.urls import path

from .views import home_view, signup_view, dashboard_view,emailmsg,add_Code_view,auth,SignUpView

app_name = "users"

urlpatterns = [

    path('', home_view, name='home'),
   # path('signup/', signup_view, name='sign-up'),
    path('sign-up/', SignUpView.as_view(), name='sign-up'),

    path('dashboard/', dashboard_view, name='dashboard'),
    path('OTP/', auth, name='OTP'),
   # path('OTP/',add_Code_view.as_view(),name='OTP'),


   # path('OTP/', emailmsg("authentcations"," Your OTP is: ","ftcode2021@gmail.com"), name='OTP'),

    
]
