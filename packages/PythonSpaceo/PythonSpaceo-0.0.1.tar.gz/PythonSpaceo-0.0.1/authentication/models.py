import email
from email.policy import default
from random import choices
from secrets import choice
from threading import local
import time
from django.db import models
# from django.forms import JSONField
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import AbstractUser
import uuid
from django.contrib.auth.models import  BaseUserManager
from django.core.validators import RegexValidator


# class UserManager(BaseUserManager):

#     def create_user(self, username, email, password=None):
#         if username is None:
#             raise TypeError('Users should have a username')
#         if email is None:
#             raise TypeError('Users should have a Email')

#         user = self.model(username=username, email=self.normalize_email(email))
#         user.set_password(password)
#         user.save()
#         return user

#     def create_superuser(self, username, email, password=None):
#         if password is None:
#             raise TypeError('Password should not be none')

#         user = self.create_user(username, email, password)
#         user.is_superuser = True
#         user.is_staff = True
#         user.save()
#         return user


AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
                  'twitter': 'twitter', 'email': 'email'}
local_language={
    'en':'english',
    'ar':'arabic'
}
# custom user
class User(AbstractUser):#AbstractUser is manage inbuilt django authsystem
    phone_message = 'Phone number must start with either 9, 8, 7 or 6 and should enter in this format: 9999955555'
    phone_regex = RegexValidator(
    regex=r'^[6-9]\d{9}$',
    message=phone_message
    )
    ten_digit = '''-> Phone number should be of 10 digits <br/> 
    -> Phone number must starts with either 9, 8, 7 or 6 <br/>
    -> Should start in this format: 9999955555
    '''


    email = models.EmailField(unique=True,null=True)
    email_verified = models.BooleanField(default=False)#for verified
    is_actives = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    mobile = models.CharField(max_length=13,null=False, validators=[phone_regex],help_text=ten_digit)
    mobile_verified_at=models.IntegerField(null=True)
    mobile_verified=models.BooleanField(default=False)
    isd_code=models.CharField(max_length=10, default='+91')
    created_at = models.IntegerField(default=int(time.time()))
    updated_at = models.IntegerField(default=int(time.time()))
    email_verified_at=models.IntegerField(null=True)
    local=models.CharField(null=True, default=local_language.get('en'), max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    def __str__(self):
        return self.username

    #for user token 
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

types = (
    ("Facebook","Facebook"),
    ("Google","Google"),
    ("Twitter","Twitter")

)
mobile=(
    ("android","android"),
    ("ios","ios"),  
    ("web","web"),
)
class Social_Login(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    social_id = models.CharField(max_length=255)
    social_type = models.CharField(default="Facebook",null=False,choices=types,max_length=25)
    social_data=models.JSONField(null=True)
class logins(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    login_type = models.CharField(null=True, default=AUTH_PROVIDERS.get('email'), max_length=50)
    ip = models.CharField(max_length=255,null=True)
    device_name = models.CharField(max_length=255) 
    device_type = models.CharField(max_length=20,choices=mobile)
    device_id = models.CharField(max_length=255) 
    fcm_key = models.CharField(max_length=255) 
    personal_access_token_id=models.CharField(max_length=500)


    created_at = models.IntegerField(default=int(time.time()))
    updated_at = models.IntegerField(default=int(time.time()))

class mobileOtp(models.Model):
    mobile=models.CharField(null=False,max_length=15)
    otp=models.CharField(null=False,max_length=6)
    counter=models.CharField(max_length=255)
    otp_expired_at=models.IntegerField(null=True)
    created_at = models.IntegerField(default=int(time.time()))
    updated_at = models.IntegerField(default=int(time.time()))


data="json data shoud be like this-[{}]"
#[{"version": "1.3.0", "plateform": "ios", "force_update": false}, {"version": "1.3.1", "plateform": "android", "force_update": true}]
class setting(models.Model):
    key=models.CharField(max_length=255)
    values=models.JSONField(help_text=data)
    created_at = models.IntegerField(default=int(time.time()))
    updated_at = models.IntegerField(default=int(time.time()))