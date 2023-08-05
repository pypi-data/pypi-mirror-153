from django.urls import path

from authentication.functional_views import ResetView, login1, passwordResetView,userdetails,mobileVersionData,currentversion
from .views import *
from rest_framework_simplejwt import views as jwt_views

# pip install git+https://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@github.com/deepakkumhar/basepack/#egg=PythonBase
# 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
urlpatterns = [
    path('settings/app-version', settingsview.as_view(), name="settingsview"),
    path('login', loginAPIView.as_view(), name="user-login"),
    path('register', registerView.as_view(), name="user-register"),
    path('social-login', Sociallogins.as_view()),
    path('password/email',RequestPasswordResetEmail.as_view()),
    path('past/logout',logoutAll.as_view()),
    path('logout',logout.as_view()),
    path('user-authentication/verify-email', VerifyUserEmail.as_view(), name='verify-email'),
    path('auth/password-reset/<uidb64>/<token>/',setpasswordview, name= 'template'),
    path('auth/login/<token_valid>',login, name= 'login'),
    path('password/reset', RequestsetPassword.as_view(), name='RequestPasswordResetEmailByOtp'),

    path('update-mobile',setMobile.as_view()),
    path('update-password', ChangePasswordView.as_view(), name='change-password'),
    path('send-otp', sendotp.as_view(), name='change-password'),
    path('verify-otp', varifyOtp.as_view(), name='varifyOtp'),
    path('update-local', local.as_view(), name='local'),
    # path('userdetails/<int:pk>',userdetails,name='userdetails'),
    path('reset/', ResetView, name="reset"),
    path('password-reset1/<uidb64>/<token>', passwordResetView, name="template"),
    path('login/<token_valid>/',login1, name='login1'),
    path('auth/post/ajax/friend/', postview, name = "post_friend"),

    path('admins/authentication/user/<int:pk>',userdetails,name='userdetails'),
    path("admins/authentication/mobile", mobileVersionData , name="deepak"),
    path('currentversion/', currentversion, name='currentversion'),
    path('verified/active/<pk>', active_group, name="approve_group"),
    path('verified/inactive/<pk>', inactive_group, name="approve_group"),
]