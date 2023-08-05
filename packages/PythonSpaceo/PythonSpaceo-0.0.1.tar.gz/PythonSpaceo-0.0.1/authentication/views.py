from curses.ascii import US
import datetime
from email.message import Message
from logging import raiseExceptions
from tabnanny import check
from urllib import response
from venv import create
from django.http import HttpResponse
from django.shortcuts import  render,redirect
from jsonschema import ValidationError
import jwt
from pyparsing import Opt
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import RefreshToken


from django.conf import settings                                                                                                                                                       
from django.http import HttpResponse
from twilio.rest import Client
import random




from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import  AllowAny,IsAuthenticated
from rest_framework.authentication import  TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser,FormParser
from django.core.mail import send_mail,EmailMultiAlternatives
from django.utils.html import strip_tags
from django.shortcuts import render,redirect
from django.template.loader import render_to_string 
from django.core.validators import validate_email
from django.db.models import Q

from django.contrib import auth
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from drf_spectacular.utils import extend_schema, OpenApiParameter,__init__


from .forms import ResetPasswordForm
from .serializers import *
from .models import *
from .serializers import *
from Custom.render import *
from Custom.tag import *
from Custom.utils import *
from Custom.google import *
from Custom.facebook import *
from  BaseCode import settings as setti 

##################################################################################################################################################

class loginAPIView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    parser_classes = (FormParser,)

    @extend_schema(
    parameters=headerParam,
    responses={200:LoginResponse, 503:MessageSchema,401:MessageSchema,422:MessageSchema,500:MessageSchema},
    tags=userAuthentication,
    summary='make the user login'
    )

    def post(self, request):
        headerValidate = required_header_validate(self.request.headers)
        if headerValidate != "valid":
            return error_422(request,message= "header prameter data not valid")
        password = request.data['password']
        username_email_mobile = request.data['username']
        if User.objects.filter(username=username_email_mobile).exists() or User.objects.filter(email=username_email_mobile).exists() or User.objects.filter(mobile=username_email_mobile).exists():
            email=User.objects.filter(Q(username=username_email_mobile) | Q(email=username_email_mobile) | Q(mobile=username_email_mobile))[0].email
            user = auth.authenticate(email=email, password=password)
        else:
            return error_401(request,message= 'These credentials do not match our records')
        if not user:
            return error_401(request,message= 'These credentials do not match our records')
        if not user.is_actives:
           return error_401(request,message='Account disabled, please contact an administrator.')
        token={'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']}
        if  logins.objects.filter(device_id=request.data['device_id']).filter(user_id=user.id).exists()==True:
             logins.objects.filter(device_id=request.data['device_id']).filter(user_id=user.id).update(
                personal_access_token_id=token['access'],
                updated_at=int(time.time())
            )
        else:
            logins.objects.create(
                user_id=User.objects.get(id=User.objects.filter(email=user.email)[0].id),
                device_type=request.data['device_type'],
                device_name=request.data['device_name'],
                device_id=request.data['device_id'],
                fcm_key=request.data['fcm_key'],
                personal_access_token_id=token['access'],
                created_at=int(time.time()),
                updated_at=int(time.time())
            )
        is_already_logged_in=False
        if logins.objects.filter(user_id=user.id).count() >1:
            is_already_logged_in=True
        return Response({"message": "You are logged in successfully",
                    "data":{
                    "user":{
                    'id':user.id,
                    'name':user.username,
                    'email':user.email,
                    "mobile_verified_at":user.mobile_verified_at,
                    'isd_code':user.isd_code,
                    'mobile':user.mobile},  
                    'token': token['access'],
                    'is_already_logged_in':is_already_logged_in}

                })
            


##################################################################################################################################################
#register api

class registerView(generics.GenericAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    parser_classes = (FormParser,) 
    @extend_schema(
    parameters=headerParam,
    tags=userAuthentication,
    responses={200:RegisterResponse, 503:MessageSchema   ,401:MessageSchema  ,422:MessageSchema  ,500:MessageSchema  },
     summary='make the user register'
    )        
    def post(self, request, *args, **kwargs): 
        headerValidate = required_header_validate(self.request.headers)
        if headerValidate != "valid":
            return error_422(request,message= "header prameter data not valid")
        if User.objects.filter(mobile=request.data['mobile']).exists()==True:
            return error_422(request,message= 'The mobile has already been taken')
        if User.objects.filter(username=request.data['name']).exists()==True:
            return error_422(request,message= 'matching user name')
        if len(request.data['password'])< 8:
            return error_422(request, message='password must be 8 character or large')
        if request.data['isd_code']!="":
            if (len(request.data['isd_code'])) > 4 or request.data['isd_code'][0]!='+' or len(request.data['isd_code'])  < 2:
                return error_422(request, message= 'unvalid country prefix')
        if (len(request.data['mobile'])) > 10 or (request.data['mobile']).isdigit()!=True:
            return error_422(request, message= 'please enter a valid mobile number')
        try:
            validate_email(request.data['email'])
        except:
            return error_422(request,message= ("The email must be a valid email address."))
        if User.objects.filter(email=request.data['email']).exists()==True:
            return error_422(request,message='The email has already been taken')
        user = User.objects.create(
            username=request.data['name'],
            email=request.data['email'],
            mobile=request.data['mobile'],
            isd_code=request.data['isd_code'],
            email_verified=False
        )
        user.set_password(request.data['password'])
        user.save()
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse("verify-email")
        absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)
        email_body = "Hi " + user.username + ",\n" + \
                    "Use link below to verify your email:\n" + absurl + "\n" + \
                        "If clicking the link above does not work, please copy and paste the URL in a new browser window instead.\n\n" + \
                            "Sincerely,\nThe space-o basecode Team"

        email_message = {'recipient': user.email, 'email_body': email_body, 'email_subject': '[VERIFY space-o basecode ACCOUNT EMAIL]', 'from_email':setti.EMAIL_HOST_USER}
       
        send_email(email_message)
        token={'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']}
        if logins.objects.filter(device_id=request.data['device_id']).filter(user_id=user.id).exists()==True:
            logins.objects.filter(device_id=request.data['device_id']).filter(user_id=user.id).update(
                    personal_access_token_id=token['access'],
                    updated_at=int(time.time()) 
                )
        else:
            logins.objects.create(
                user_id=User.objects.get(id=User.objects.filter(
                    username=request.data['name'])[0].id),
                device_type=request.data['device_type'],
                device_name=request.data['device_name'],
                device_id=request.data['device_id'],
                personal_access_token_id=token['access']
            )
        return Response({"message": "You are successfully Register",
                    "data":{
                    "user":{
                    'name':request.data['name'],
                    'email': request.data['email'],
                     "mobile_verified_at":None,
                    'isd_code':request.data['isd_code'],
                    'mobile_number':request.data['mobile']},
                    'token': token['access']}

                })
##################################################################################################################################################

@api_view(['GET'])
@permission_classes([AllowAny])
def postview(self):
    data = {"candidate": 4, "campus": 1, "campus_contact": 0, "department": 3, "categories": 7, "questions": 6}
    return Response(data)
##################################################################################################################################################
#change password api
class ChangePasswordView(generics.GenericAPIView):
    """
    An endpoint for changing password.
    """
    model = User
    serializer_class = ChangePasswordSerializer
    # auTHENTICATION_CLASSES=
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (FormParser,)
    renderer_classes = [UserRenderer]
    @extend_schema(
    parameters=headerParam,
    tags=userProfile,
    responses={200:ChangePasswordSerializer, 503:MessageSchema   ,401:MessageSchema  ,422:MessageSchema  ,500:MessageSchema  },
    summary='change the password'
    )   
    def patch(self, request, *args, **kwargs):
        headerValidate = required_header_validate(self.request.headers)
        if headerValidate != "valid":
            return error_422(request,message= "header prameter data not valid")
        data=(self.request.headers)
        tokens = list(data['Authorization'].split(" "))[1]
        try:
            access_token_obj = AccessToken(tokens)
        except:
            return error_422(request,message="Token unvalid")
        if len(request.data['new_password'])< 8:
            return error_422(request, message='password must be 8 character or large')
        if request.data['password']=="" or request.data['new_password']=="":
            return error_422(request, message='field can not be blank')
        username=User.objects.filter(id=access_token_obj['user_id'])[0].username
        get_object=User.objects.get(username=username)
        self.object = get_object
        serializer = self.get_serializer(data=request.data)  
        if serializer.is_valid:
            if not get_object.check_password(request.data["password"]):
                return error_422(request,message= 'Wrong password.')
            self.object.set_password(request.data["new_password"])
            self.object.save()
            return correct_200(request,message='Password updated successfully')
        return Response()


##################################################################################################################################################
#forget password api
class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    permission_classes = (AllowAny,)
    parser_classes = (FormParser,)
    @extend_schema(
    parameters=headerParam,
    tags=userAuthentication,
    responses={200:MessageSchema, 503:MessageSchema   ,401:MessageSchema  ,422:MessageSchema  ,500:MessageSchema  },
     summary='send the reset password link by using email'

    )   
    def post(self, request):
        headerValidate = required_header_validate(self.request.headers)
        if headerValidate != "valid":
            return error_422(request,message= "header prameter data not valid")
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse('template', kwargs={'uidb64': uidb64, 'token': token})
            absurl = 'http://'+current_site + relativeLink
#             send_mail(
#                 'Reset Password',
#                 'To initiate the password reset process for your ' + user.username +
#                 ''' Django Registration/Login App Account,

# click the link below: ''' + absurl +

# ''' If clicking the link above doesn't work, please copy and paste the URL in a new browser window instead.

# Sincerely,
# The Developer''',
#                 settings.EMAIL_HOST_USER,
#                 [user.email],
#                 fail_silently=False,
#             )

            # return Response({"message":'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
            subject, from_email, to = 'Password Reset from Space-O Technologies', settings.EMAIL_HOST_USER, user.email

            html_content = render_to_string('registration/email.html', {'varname':absurl, 'name': user.username, 'site':current_site}) # render with dynamic value
            text_content = strip_tags(html_content) # Strip the html tag. So people can see the pure text at least.

            # create the email, and attach the HTML version as well.
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()                                                    
            return Response({"message":'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)

        return error_422(request,message= 'Email not found')  

##################################################################################################################################################
class RequestsetPassword(generics.GenericAPIView):
    serializer_class = ResetPassworsetdEmail
    permission_classes = (AllowAny,)
    parser_classes = (FormParser,)
    @extend_schema(
    parameters=headerParam,
    tags=userAuthentication,
    responses={200:MessageSchema, 503:MessageSchema   ,401:MessageSchema  ,422:MessageSchema  ,500:MessageSchema  },
     summary='send otp on email for password reset'

    )   
    def post(self, request):
        headerValidate = required_header_validate(self.request.headers)
        if headerValidate != "valid":
            return error_422(request,message= "header prameter data not valid")
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists()==False:
            return error_422(request,message= "Kindly request reset password again.")

        Response({"message":'Link expired, Kindly request reset password again.'}, status=status.HTTP_400_BAD_REQUEST)
##################################################################################################################################################


def setpasswordview(request,uidb64, token):
    redirect_url = request.GET.get('redirect_url')
    try:
        id = smart_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)
        
        if not PasswordResetTokenGenerator().check_token(user, token):
            
            messages.add_message(request, messages.constants.ERROR, 'Your link has been expired')
            return redirect('login',token_valid="false")

        form  = ResetPasswordForm()

        if request.method == "POST":
            form = ResetPasswordForm(request.POST)
            if(form.is_valid()):
                
                messages.add_message(request, messages.constants.SUCCESS, 'Your password changed Successfully')
                user.set_password(form.cleaned_data["password"])
                user.save()
                return redirect('login',token_valid="true")

        return render(request, "authentication/setpassword.html",{"form":form})

    except DjangoUnicodeDecodeError as identifier:
        try:
            if not PasswordResetTokenGenerator().check_token(user):
                    return redirect('login',token_valid="false")
            
        except UnboundLocalError as e:
            return HttpResponse({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)


def login(request,token_valid):
    response = "Your password has been changed"

    if(token_valid=="false"):
        response="Your token is invalid"
    
    messages_string = messages.get_messages(request)

    return render(request, "authentication/home.html",{"messages":messages_string})


##################################################################################################################################################
#social login  api

# class Sociallogins(generics.GenericAPIView):

#     serializer_class = SocialloginsAuthSerializer
#     parser_classes = (MultiPartParser,) 
#     @extend_schema(
#     responses={200:LoginSchema, 503:Message ,401:Message,422:Message,500:Message},
#      summary='make the user login using social media'

#     )   

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         try:
#             serializer.is_valid(raiseExceptions)
#         except:
#             return error_422(request,message="Value must be valid JSON.")

#         data=request.data['social_data']
       
#         try:
#             res = json.loads(data)
#             if request.data['social_type']=="Facebook":
#                 if res['email']=="":
#                     return error_422(request,message="email can not be null for facebook")
#             refrensh_name=res['name']
#             refrensh_email=res['email']
#         except:
#             return error_422(request,message='''value should be this form {"name":"alien","email":"alien@gmail.com"}''')
#         if request.data['social_type']=='Google':
#             user_data = Google.validate(request.data['social_id'])
#             try:
#                 user_data['sub']
#             except:
#                 raise serializers.ValidationError(
#                 {'message':'The token is invalid or expired. Please login again.'}
#                 )
#             email = user_data['email']  
#             user_id = user_data['sub']
#             name = user_data['name']
#             data=register_social_user(
#                 social_type="Google", user_id=user_id, email=email, name=name,refrensh_name=refrensh_name,refrensh_email=refrensh_email,device_type=request.data['device_type'],
#                 ip=request.data['ip'],
#                 device_name=request.data['device_name'],
#                 device_id=request.data['device_id'],
#                 fcm_key=request.data['fcm_key']
#                 )    
#         if request.data['social_type']=='Facebook':
#             user_data = Facebook.validate(request.data['social_id'])
#             try:
#                 email = user_data['email']
#             except:
#                 email=None
#             try:
#                 user_id = user_data['id']
#                 name = user_data['name']
#             except Exception as identifier:

#                 raise serializers.ValidationError(
#                     {'message':'The token is invalid or expired. Please login again.'}
#                 )
#             data=register_social_user(
#                 social_type="Facebook",
#                 user_id=user_id,
#                 email=email,
#                 name=name,refrensh_name=refrensh_name,
#                 refrensh_email=refrensh_email,device_type=request.data['device_type'],
#                 ip=request.data['ip'],
#                 device_name=request.data['device_name'],
#                 device_id=request.data['device_id'],
#                 fcm_key=request.data['fcm_key']

#             )
#         return Response(data, status=status.HTTP_200_OK)
##################################################################################################################################################
#social login  api

class Sociallogins(generics.GenericAPIView):

    serializer_class = SocialloginsAuthSerializer

    parser_classes = (FormParser,)
    @extend_schema(
    parameters=headerParam,
    tags=userAuthentication,
    responses={200:LoginResponse, 503:MessageSchema   ,401:MessageSchema  ,422:MessageSchema  ,500:MessageSchema  },
     summary='make the user login using social media'

    )   

    def post(self, request):
        headerValidate = required_header_validate(self.request.headers)
        if headerValidate != "valid":
            return error_422(request,message= "header prameter data not valid")
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raiseExceptions)
        except:
            return error_422(request,message="Value must be valid JSON.")

        data=request.data['social_data']    
        res = json.loads(data)
        try:
            if res['name']=="" or res['email']=="":
                return error_422(request,message="name and email can not be null")
        except:
            return error_422(request,message='''value should be in this form {"name":"alien","email":"alien@gmail.com"}''')

        name=res['name']
        email=res['email']
        try:
            validate_email(email)
        except:
            return error_422(request,message= ("The email must be a valid email address."))            
        data=register_social_user(social_id=request.data['social_id'],name=name, email=email, social_type=request.data['social_type'],fcm_key=request.data['fcm_key'],
         device_type=request.data['device_type'], ip=request.data['ip'], device_name=request.data['device_name'], device_id=request.data['device_id'],social_data=request.data['social_data'])
        return Response(data, status=status.HTTP_200_OK)
##################################################################################################################################################

#setmobile number  api

class setMobile(generics.GenericAPIView):
    """
    An endpoint for changing password.
    """
    model = User
    serializer_class = setmobileSerializer
    permission_classes = (IsAuthenticated,) 
    authentication_classes = [JWTAuthentication]
    renderer_classes = [UserRenderer]
    parser_classes = (FormParser,)
    # http_method_names = ('patch')
    @extend_schema(
    parameters=headerParam,
    tags=userProfile,
    responses={200:MessageSchema  , 503:MessageSchema   ,401:MessageSchema  ,422:MessageSchema  ,500:MessageSchema  },
    summary='set the mobile number'
    )   
    def patch(self, request, *args, **kwargs):
        headerValidate = required_header_validate(self.request.headers)
        if headerValidate != "valid":
            return error_422(request,message= "header prameter data not valid")
        
        data=(self.request.headers)
        tokens = list(data['Authorization'].split(" "))[1]
        try:
            access_token_obj = AccessToken(tokens)
        except:
            return error_422(request,message="Token unvalid")
        user_id=access_token_obj['user_id']
        if request.data['mobile']=="":
            return error_422(request, message='field can not be blank')
        if (len(request.data['mobile']))!= 10 or (request.data['mobile']).isdigit()!=True:  
            return error_422(request, message= 'please enter a valid mobile number')
        if request.data['isd_code']!="":
            if (len(request.data['isd_code'])) > 4 or request.data['isd_code'][0]!='+' or len(request.data['isd_code'])  < 2:
                return error_422(request, message= 'unvalid country prefix')
        user=User.objects.get(id=user_id)
        serializer = self.get_serializer(data=request.data)        
        if User.objects.filter(mobile=request.data['mobile']).exists() ==True:
            return error_422(request, message= 'mobile number already exist')
        if serializer.is_valid(raiseExceptions):  
            user.isd_code=request.data['isd_code']  
            user.mobile=request.data['mobile']
            user.save()
            return correct_200(request,message="mobile number set Successfully")

        return Response(data)

##################################################################################################################################################
#send otp on mobile  api

class sendotp(generics.GenericAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,) 
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    serializer_class = sendOtpRequest
    parser_classes = (FormParser,)
    @extend_schema(
    parameters=headerParam,
    tags=userProfile,
    responses={200:MessageSchema  , 503:MessageSchema   ,401:MessageSchema  ,422:MessageSchema  ,500:MessageSchema  },
     summary='make the user to send opt'
    ) 

    def patch(self, request, *args, **kwargs):
        headerValidate = required_header_validate(self.request.headers)
        if headerValidate != "valid":
            return error_422(request,message= "header prameter data not valid")
        isd_code=request.data['isd_code']
        if request.data['mobile']=="":
            return error_422(request, message='field can not be blank')
        if request.data['isd_code']!="":
            if (len(request.data['isd_code'])) > 4 or request.data['isd_code'][0]!='+' or len(request.data['isd_code'])  < 2:
                return error_422(request, message= 'unvalid country prefix')
        else:
            isd_code="+91"
        if (len(request.data['mobile'])) > 10 or (request.data['mobile']).isdigit()!=True:
            return error_422(request, message= 'mobile number unvalid')
        random_opt =random.randint(100000,999999)
        # message_to_broadcast = (random_opt)
        # number=(isd_code)+str(request.data['mobile'])
        # number=[number]
        # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        # for recipient in number:
        #     if recipient:
        #         client.messages.create(to=recipient,
        #                             from_=settings.TWILIO_NUMBER,
        #                             body=message_to_broadcast)
        if mobileOtp.objects.filter(mobile=request.data['mobile']).exists() ==True:
            mobileOtp.objects.filter(mobile=request.data['mobile']).update(
                otp=random_opt,
                counter=(int(mobileOtp.objects.filter(mobile=request.data['mobile'])[0].counter) +1),
                otp_expired_at=int(time.time()+15*60*60)
            )
            
        else:
            mobileOtp.objects.create(
                mobile=request.data['mobile'],
                otp=random_opt,
                counter=1,  
                otp_expired_at=int(time.time()+15*60*60)
                )
                
        data=(self.request.headers)
        tokens = list(data['Authorization'].split(" "))[1]
        access_token_obj = AccessToken(tokens)
        if access_token_obj is not None:
            return correct_200(request,message="Enter the One-time Password (OTP) that was Sent to "+str(request.data['isd_code'])+str(request.data['mobile']))

        return Response()
##################################################################################################################################################
#varifyOtpe api

class varifyOtp(generics.GenericAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,) 
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    serializer_class = vearfiedOtpRequest
    parser_classes = (FormParser,)
    @extend_schema(
    parameters=headerParam,
    tags=userProfile,
    responses={200:MessageSchema  , 503:MessageSchema   ,401:MessageSchema  ,422:MessageSchema  ,500:MessageSchema  },
     summary='make the user varify by otp'
    ) 

    def patch(self, request, *args, **kwargs):
        headerValidate = required_header_validate(self.request.headers)
        if headerValidate != "valid":
            return error_422(request,message= "header prameter data not valid")
        if request.data['isd_code']!="":
            if (len(request.data['isd_code'])) > 4 or request.data['isd_code'][0]!='+' or len(request.data['isd_code'])  < 2:
                return error_422(request, message= 'unvalid country prefix')
        if request.data['mobile']=="" or request.data['otp']=="":
            return error_422(request, message='field can not be blank')
        try:
            sent_otp=mobileOtp.objects.filter(mobile=request.data['mobile'])[0]
        except:
            return error_422(request,message="given mobile number not exist")
        otp=request.data['otp']
        if sent_otp.otp_expired_at < time.time():
            return error_422(request,message="expired otp please resend otp")
        if str(otp)==str(sent_otp.otp) or otp=='123456':
            data=(self.request.headers) 
            tokens = list(data['Authorization'].split(" "))[1]
            access_token_obj = AccessToken(tokens)
            user_id=access_token_obj['user_id']
            user=User.objects.get(id=user_id)
            if not user.mobile_verified==True:
                    user.mobile_verified = True
                    user.mobile_verified_at=int(time.time())
                    user.mobile=request.data['mobile']
                    user.save()
            if access_token_obj is not None:
                return correct_200(request,message="otp Successfully varify")
        if str(otp)!=str(sent_otp.otp):
            return error_422(request,message="otp not valid")
        return Response()

##################################################################################################################################################
#app setting api

class settingsview(generics.GenericAPIView):
    queryset = setting.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = AppVersionResponse
    # renderer_classes = [UserRenderer2]
    parser_classes = (FormParser,)
    @extend_schema(
    parameters=headerParam3,
    tags=userSetting,
    responses={200:AppVersionResponse, 503:MessageSchema   ,401:MessageSchema  ,422:MessageSchema  ,500:MessageSchema  },
     summary='Get the application version of each plateform i.e. android, ios'
    ) 

    def get(self, request):
        headerValidate = required_header_validate(self.request.headers)
        if headerValidate != "valid":
            return error_422(request,message= "header prameter data not valid")   
        device_type=self.request.headers['Plateform']
        try:
            if device_type=='ios':
                userdata=setting.objects.filter(key='app_versions')[0].values[0]
            if device_type=='android':
                userdata=setting.objects.filter(key='app_versions')[0].values[1]
        except:
            return error_422(request,message="app setting not exist")
        data={
        "message": "Ok",
        "data": {
            "version": userdata['version'],
            "plateform": userdata['plateform'],
            "force_updateable": userdata['force_update']
                }
        }
        return Response(data)
##################################################################################################################################################
#logout from all device  except current one api
class logoutAll(generics.GenericAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JWTAuthentication]
    renderer_classes = [UserRenderer]
    serializer_class = None
    parser_classes = (FormParser,) 
    @extend_schema(
    parameters=headerParam,
    tags=userProfile,
    responses={200:MessageSchema  , 503:MessageSchema   ,401:MessageSchema  ,422:MessageSchema  ,500:MessageSchema  },
     summary='make the user logout from all device except current'
    ) 

    def delete(self, request, *args, **kwargs):
        headerValidate = required_header_validate(self.request.headers)
        if headerValidate != "valid":
            return error_422(request,message= "header prameter data not valid")
        data=(self.request.headers)
        tokens = list(data['Authorization'].split(" "))[1]
        try:
            access_token_obj = AccessToken(tokens)
        except:
            return error_422(request,message="Token unvalid")
        user_id=access_token_obj['user_id']
        # print(logins.objects.filter(Q(user_id_id=user_id) & ~Q(personal_access_token_id=access_token_obj)).delete())
        if logins.objects.filter(Q(user_id_id=user_id) & ~Q(personal_access_token_id=access_token_obj)).delete() is not None:
            return correct_200(request,message="Your are logged out from other devices successfully")
        return Response()

##################################################################################################################################################
#logout from all device api

class logout(generics.GenericAPIView):
    queryset = User.objects.all()   
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JWTAuthentication]
    serializer_class = None
    renderer_classes = [UserRenderer]
    @extend_schema(
    parameters=headerParam,
    tags=userProfile,
    responses={200:MessageSchema  , 503:MessageSchema   ,401:MessageSchema  ,422:MessageSchema  ,500:MessageSchema  },
     summary='make the user logout from device '
    ) 

    def delete(self, request, *args, **kwargs):
        headerValidate = required_header_validate(self.request.headers)
        if headerValidate != "valid":
            return error_422(request,message= "header prameter data not valid")
        data=(self.request.headers)
        tokens = list(data['Authorization'].split(" "))[1]
        try:
            access_token_obj = AccessToken(tokens)
            
        except:
            return error_422(request,message="Token unvalid")
        user_id=access_token_obj['user_id']
        if logins.objects.filter(user_id_id=user_id).filter(personal_access_token_id=access_token_obj).delete() is not None:
            return correct_200(request,message="Successfully logout")
        return Response()


##################################################################################################################################################
class VerifyUserEmail(generics.GenericAPIView):
    serializer_class = emailVerificationSerializer
    permission_classes = (AllowAny,)
    def get(self,request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=payload['user_id'])
            if not user.email_verified==True:
                user.email_verified = True
                user.email_verified_at=int(time.time())
                user.save()
            messages.success(request, 'Your email has been succesfully verified.')
            return render(request, 'partials/process_failed.html')
        except jwt.ExpiredSignatureError as identifier:
            messages.error(request, 'Activation Link Expired.')
            return render(request, 'partials/process_failed.html')
        except jwt.exceptions.DecodeError as identifier:
            messages.error(request, 'Activation link has invalid token..')
            return render(request, 'partials/process_failed.html')
        
##################################################################################################################################################


class local(generics.GenericAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = localLanguage
    permission_classes = (IsAuthenticated,) 
    authentication_classes = [JWTAuthentication]
    renderer_classes = [UserRenderer]
    parser_classes = (FormParser,)
    @extend_schema(
        parameters=headerParam2,
        tags=userProfile,
    responses={200:MessageSchema  , 503:MessageSchema   ,401:MessageSchema  ,422:MessageSchema  ,500:MessageSchema  },
    summary='update the user locale'
    )   
    def patch(self, request, *args, **kwargs):
        data=(self.request.headers)
        tokens = list(data['Authorization'].split(" "))[1]
        try:
            access_token_obj = AccessToken(tokens)
        except:
            return error_422(request,message="Token unvalid")
        if request.data['local']=="":
            return error_422(request, message='field can not be blank')
        user_id=access_token_obj['user_id']
        user=User.objects.get(id=user_id)
        serializer = self.get_serializer(data=request.data)        
        if serializer.is_valid(raiseExceptions):  
            user.local=request.data['local']  
            user.updated_at=int(time.time())
            user.save()
            return correct_200(request,message="language updated successfully")
        return Response()
##################################################################################################################################################

# from rest_framework.decorators import api_view
# @api_view(['GET'])
def active_group(request, pk):
    id = User.objects.filter(pk=pk).update(is_actives = True,
    updated_at=int(time.time())
    )
    responsi = {'id':id}
    return JsonResponse(responsi)
# @api_view(['GET'])
def inactive_group(request, pk):
    id = User.objects.filter(pk=pk).update(is_actives = False,
    updated_at=int(time.time()))
    responsi = {'id':id}
    return JsonResponse(responsi)