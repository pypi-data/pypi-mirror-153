import email
from email import message
from email.policy import default
from ensurepip import version
from enum import unique
from lib2to3.pgen2 import token
from statistics import mode
from attr import field, fields
from django.contrib import auth
from django.contrib.auth.password_validation import validate_password
from django.http import HttpResponse
from pkg_resources import require

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.validators import UniqueValidator

from .models import Social_Login, User, logins
from .register import register_social_user
import os

mobile = (
    ("android", "android"),
    ("ios", "ios"),
    ("web", "web"),
)
types = (
    ("Facebook","Facebook"),
    ("Google","Google"),
    ("Twitter","Twitter")

)
local_language={
    'en':'english',
    'ar':'arabic'
}
##################################################################################################################################################


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True,help_text="username can either be email, mobile number or username. mobile must be  without country prefix like- 9999999999")
    password = serializers.CharField(
        max_length=128, min_length=8, write_only=True)
    device_name = serializers.CharField()
    device_type = serializers.ChoiceField(required=True, choices=mobile)
    device_id = serializers.CharField()
    fcm_key = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'password',
                  'device_name', 'device_type', 'device_id', 'fcm_key']

##################################################################################################################################################


# user register api serializers


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    name=serializers.CharField()
    device_name = serializers.CharField()   
    device_type = serializers.ChoiceField(required=True, choices=mobile)
    device_id = serializers.CharField()
    isd_code=serializers.CharField(default='+91')       

    class Meta:
        model = User
        fields = ('name', 'email', 'password','isd_code', 'mobile',
                  'device_name' ,'device_id', 'device_type')

##################################################################################################################################################


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    """
    Serializer for password change endpoint.
    """
    password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

##################################################################################################################################################


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']

##################################################################################################################################################
class ResetPassworsetdEmail(serializers.Serializer):
    token=serializers.CharField()
    email = serializers.CharField()


##################################################################################################################################################

# response serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


##################################################################################################################################################


class SocialloginsAuthSerializer(serializers.ModelSerializer):
    social_id = serializers.CharField(required=True)
    social_type = serializers.ChoiceField(required=True, choices=types)
    device_type = serializers.ChoiceField(required=True, choices=mobile)
    ip = serializers.CharField(required=True)
    device_name = serializers.CharField(required=True)
    device_id = serializers.CharField(required=True)
    fcm_key = serializers.CharField(required=False)

    social_data=serializers.JSONField(default={"name":"alien","email":"alien@gmail.com"})
    class Meta:
        model = Social_Login
        fields = ['social_id','social_data', 'social_type',
                  'device_type', 'ip', 'device_name', 'device_id', 'fcm_key']


##################################################################################################################################################
class sendOtpRequest(serializers.Serializer):
    isd_code=serializers.CharField(default='+91')
    mobile=serializers.CharField()

##################################################################################################################################################
class vearfiedOtpRequest(serializers.Serializer):
    isd_code=serializers.CharField(default='+91')
    mobile=serializers.CharField()
    otp=serializers.CharField()

##################################################################################################################################################

class User(serializers.ModelSerializer):
    name=serializers.CharField()
    mobile_verified_at=serializers.CharField()
    class Meta:
        model=User
        fields=['id','name','email','mobile_verified_at','isd_code','mobile']
class  RegisterData(serializers.Serializer):
    user=User()
    token=serializers.CharField()
class RegisterResponse(serializers.Serializer):  
    message=serializers.CharField()
    data=	RegisterData()

class MessageSchema(serializers.Serializer):
    message=serializers.CharField()
class massage(serializers.Serializer):
    massage=serializers.CharField()

##################################################################################################################################################
class 	LoginData(serializers.Serializer):
    user=User()
    is_already_logged_in=serializers.BooleanField()
    token=serializers.CharField()
class LoginResponse(serializers.Serializer):  
    message=serializers.CharField()
    data=LoginData()

class MessageSchema(serializers.Serializer):
    message=serializers.CharField()
class massage(serializers.Serializer):
    massage=serializers.CharField()

##################################################################################################################################################


class setmobileSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    isd_code=serializers.CharField(default='+91')  
    mobile=serializers.CharField(required=True)
##################################################################################################################################################
class 	AppVersion(serializers.Serializer):
    version=serializers.CharField()
    plateform=serializers.CharField()
    force_updateable=serializers.BooleanField()
class AppVersionResponse(serializers.Serializer):
    massage=serializers.CharField()
    data=AppVersion()



##################################################################################################################################################
class emailVerificationSerializer(serializers.Serializer):
    token=serializers.CharField()
    email=serializers.CharField()

##################################################################################################################################################
class localLanguage(serializers.Serializer):
    local = serializers.ChoiceField(required=True, choices=local_language)
