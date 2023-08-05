import datetime
from lib2to3.pgen2 import token
from time import time
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.utils.html import strip_tags
from django.shortcuts import render,redirect
from django.template.loader import render_to_string 
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError

from .models import User,logins,setting
from rest_framework import status

def passwordResetView(request,uidb64, token):
    try:
        MIN_LENGTH = 8
        id = smart_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)
        
        if not PasswordResetTokenGenerator().check_token(user, token):
            
            messages.add_message(request, messages.constants.ERROR, 'Your link has been expired')
            return redirect('login1',token_valid="false")
        
        if request.method == "POST":
            # form = ResetPasswordForm(request.POST)
            password = request.POST["password1"]
            # At least MIN_LENGTH long
            if len(password) < MIN_LENGTH:
                return render(request, "registration/recover-password.html", {'min_len': f"The new password must be at least {MIN_LENGTH} characters long."})

            # At least one letter and one non-letter
            first_isalpha = password[0].isalpha()
            if all(c.isalpha() == first_isalpha for c in password):
                return render(request, "registration/recover-password.html", {'min_len': "The new password must contain at least one letter and at least one digit or" \
                                            " punctuation character."})
            
            confirm_password = request.POST["password2"]

            if password != confirm_password:
                return render(request, "registration/recover-password.html", {'Wrong': "Password Does not match"})
            # if(form.is_valid()):
                
            messages.add_message(request, messages.constants.SUCCESS, 'Your password changed Successfully')
            user.set_password(confirm_password)
            user.save()
            return redirect('login1',token_valid="true")
        return render(request, "registration/recover-password.html", {'uidb64': uidb64})

    except DjangoUnicodeDecodeError as identifier:
        try:
            if not PasswordResetTokenGenerator().check_token(user):
                    return redirect('login1',token_valid="false")
            
        except UnboundLocalError as e:
            return HttpResponse({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)

def ResetView(request):
    if request.method == 'POST':
        try:
            email = request.POST['email']
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse('template', kwargs={'uidb64': uidb64, 'token': token})
            absurl = 'http://'+current_site + relativeLink
            subject, from_email, to = 'Password Reset from Space-O Technologies', settings.EMAIL_HOST_USER, user.email

            html_content = render_to_string('registration/email.html', {'varname':absurl, 'name': user.username, 'site':current_site}) # render with dynamic value
            text_content = strip_tags(html_content) # Strip the html tag. So people can see the pure text at least.

            # create the email, and attach the HTML version as well.
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()                                                    
            return render(request, 'registration/password_reset_form.html', {"EmailSend": "We’ve emailed you instructions for setting your password, if an account exists with the email you entered. You should receive them shortly. If you don’t receive an email, please make sure you’ve entered the address you registered with, and check your spam folder."})
        except User.DoesNotExist:
            messages.add_message(request, messages.constants.ERROR, 'Email Does not Exist')
            return redirect('reset')

    return render(request, 'registration/password_reset_form.html')

def login1(request,token_valid):
    if(token_valid=="false"):
        return render(request, 'registration/error.html')

    return redirect('admin:login')

def error_404_view(request, exception):
    return render(request,'404.html')


from BaseCode.settings import SIMPLE_JWT
def userdetails(request,pk):
    userData=User.objects.filter(id=pk)
    first_name=userData[0].first_name
    last_name=userData[0].last_name
    userData.update(
        first_name='-',
        last_name='-'
    )

    if userData[0].mobile_verified_at is not None:
        userData.update(
            first_name=(datetime.datetime.fromtimestamp(userData[0].mobile_verified_at))
        )
    if userData[0].email_verified_at is not None:
        userData.update(
            last_name=datetime.datetime.fromtimestamp(userData[0].email_verified_at)
        )  



    userData=userData[0]
    User.objects.filter(id=pk).update(
        first_name=first_name,
        last_name=last_name
    )
    
    diviceDataa=logins.objects.filter(user_id=pk).values('device_type','device_name','updated_at')
    diviceData=[]
    token_expired=(SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].days)*24*60*60
    for value in diviceDataa:
        diviceData.append({
            "device_type":value["device_type"],
            "device_name":value["device_name"],
            "updated_at":datetime.datetime.fromtimestamp(value['updated_at']) ,
            "expired_at":datetime.datetime.fromtimestamp(int(value['updated_at'])+token_expired)
        })
    return render(request,'userDetails.html', {'userData': userData,'diviceData':diviceData})   


def currentversion(request):
    data=setting.objects.filter(key='app_versions')[0].values
    ios=data[0]
    android=data[1]
    context = {'android':android,'ios':ios}
    return JsonResponse(context)
import time
from django.http import HttpResponseRedirect
def mobileVersionData(request):   
    if(request.method=="POST"):
        android_version=(request.POST['android[version]'])
        ios_version=(request.POST['ios[version]'])    
        try:
            ios_force_update=(request.POST['iosforce'])
            ios_force_update=True
        except:
            ios_force_update=False
        try:
            android_force_update=(request.POST["androidforce"])
            android_force_update=True
        except:
              android_force_update=False
        if android_version=="" or ios_version=="":
            error="version can not be null"
            return  render(request,"mobileversion.html",{'error':error})
        if android_version[0].isalpha()==True or android_version[2].isalpha()==True or android_version[4].isalpha()==True  or ios_version[0].isalpha()==True or ios_version[2].isalpha()==True or ios_version[4].isalpha()==True:
            error="Version format is invalid"
            return  render(request,"mobileversion.html",{'error':error})     
        if (len(android_version)) >5 or (len(android_version)) < 5 or (len(ios_version)) >5 or (len(ios_version)) < 5:
            error="Version format is invalid"
            return  render(request,"mobileversion.html",{'error':error})    
        data=[]
        data=[{"version": ios_version, "plateform": "ios", "force_update": ios_force_update}, {"version": android_version, "plateform": "android", "force_update": android_force_update}]
        setting.objects.update(
             
            updated_at=int(time.time()),
            key="app_versions",
            values=data,
        )    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))