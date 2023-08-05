from lib2to3.pgen2 import token
from django.contrib.auth import authenticate
from requests import Response, request
from authentication.models import User
from .models import *
import os
import random

# this is used to create a random username by name


def generate_username(name):

    username = "".join(name.split(' ')).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)
# for token


# def tokens(username):
#     user = User.objects.get(username=username)
#     return {
#         'refresh': user.tokens()['refresh'],
#         'access': user.tokens()['access']
#     }


def tokens(email):
    user = User.objects.get(email=email)
    return {
        'refresh': user.tokens()['refresh'],
        'access': user.tokens()['access']
    }
# for login device data
def device_data(user_id, fcm_key, device_type, ip, device_name, device_id, social_type,personal_access_token_id):
        if logins.objects.filter(device_id=device_id).filter(user_id=user_id).exists()==True:
            logins.objects.filter(device_id=device_id).filter(user_id=user_id).update(
                    personal_access_token_id=personal_access_token_id,
                    updated_at=int(time.time())
                )
        else:
            logins.objects.create(
                user_id=User.objects.get(id=user_id),
                device_type=device_type,
                device_name=device_name,
                device_id=device_id,
                personal_access_token_id=personal_access_token_id,
                fcm_key=fcm_key,
                ip=ip,
                login_type=social_type
            )
# for user register


# def register_social_user(social_type, user_id, email, name, refrensh_name, refrensh_email, fcm_key, device_type, ip, device_name, device_id):
#     filtered_user_by_social_id = Social_Login.objects.filter(social_id=user_id)
#     filtered_user_by_user_email_in_User = User.objects.filter(
#         email=refrensh_email)

#     if email is None:
#         if filtered_user_by_social_id.exists():
#             if social_type == filtered_user_by_social_id[0].social_type:
#                 user_id = filtered_user_by_social_id[0].user_id.id
#                 user = User.objects.filter(id=user_id)
#                 email = None
#                 token =tokens(user[0].username)
#                 device_data(user_id=user_id, social_type=social_type, fcm_key=fcm_key,
#                             device_type=device_type, ip=ip, device_name=device_name, device_id=device_id,personal_access_token_id=token['access'])
#                 return{
#                     "message": "You are logged in successfully",
#                     "data": {
#                         "user": {
#                             'id': user[0].id,
#                             'isd_code': user[0].isd_code,
#                             'mobile': user[0].mobile,
#                             'name': user[0].username,
#                             'email': user[0].email},
#                         'token': token}

#                 }
#         if filtered_user_by_social_id.exists() == False and filtered_user_by_user_email_in_User.exists() == True:
#             username = User.objects.filter(email=refrensh_email).values('username')[
#                 0].get('username')
#             userid = filtered_user_by_user_email_in_User[0].id
#             Social_Login.objects.create(
#                 user_id=User.objects.get(id=userid),
#                 name=refrensh_name,
#                 email=refrensh_email,
#                 social_id=user_id,
#                 social_type=social_type,
#             )
#             token=tokens(username)
#             device_data(user_id=userid, social_type=social_type,
#                         fcm_key=fcm_key, device_type=device_type, ip=ip, device_name=device_name, device_id=device_id,personal_access_token_id=token['access'])
#             return{
#                 "message": "You are logged in successfully",
#                 "data": {
#                     "user": {
#                         'id': filtered_user_by_user_email_in_User[0].id,
#                         'isd_code': filtered_user_by_user_email_in_User[0].isd_code,
#                         'mobile': filtered_user_by_user_email_in_User[0].mobile,
#                         'name': username,
#                         'email': filtered_user_by_user_email_in_User[0].email,
#                         'token': token}}

#             }
#         else:
#             user = User.objects.create(
#                 email=refrensh_email,
#                 first_name=refrensh_name,
#                 username=generate_username(name),
#                 password="random string",
#                 is_verified=True
#             )
#             user.save()
#             userid = user.id
#             Social_Login.objects.create(
#                 user_id=User.objects.get(id=userid),
#                 name=refrensh_name,
#                 email=refrensh_email,
#                 social_id=user_id,
#                 social_type=social_type,
#             )
#             token=tokens(user.username)
#             device_data(user_id=user_id, social_type=social_type, fcm_key=fcm_key,
#                         device_type=device_type, ip=ip, device_name=device_name, device_id=device_id,personal_access_token_id=token['access'])
#             return{
#                 "message": "You are logged in successfully",
#                 "data": {
#                     "user": {
#                         'id': user.id,
#                         'isd_code': user.isd_code,
#                         'mobile': user.mobile,
#                         'name': user.username,
#                         'email': refrensh_email},
#                     'token': token}

#             }

#     else:
#         filtered_user_by_user_email_in_User = User.objects.filter(email=email)
#         # filtered_user_by_user_email_in_User =
#         filtered_user_by_user_social_id_in_sociallogin = Social_Login.objects.filter(
#             social_id=user_id)

#         # if filtered_user_by_user_email_in_User.exists() and filtered_user_by_user_social_id_in_sociallogin.exists():
#         if filtered_user_by_user_social_id_in_sociallogin.exists() == True:
#             # username = User.objects.filter(email=email).values('username')[
#             #     0].get('username')
#             # print(filtered_user_by_user_social_id_in_sociallogin[0].user_id_id)
#             filtered_user_by_user_email_in_User = User.objects.filter(
#                 id=filtered_user_by_user_social_id_in_sociallogin[0].user_id_id)
#             token=tokens(filtered_user_by_user_email_in_User[0].username)
#             device_data(user_id=filtered_user_by_user_email_in_User[0].id, social_type=social_type,
#                         fcm_key=fcm_key, device_type=device_type, ip=ip, device_name=device_name, device_id=device_id,personal_access_token_id=token['access'])
#             return{
#                 "message": "You are logged in successfully",
#                 "data": {
#                     "user": {
#                         'id': filtered_user_by_user_email_in_User[0].id,
#                         'isd_code': filtered_user_by_user_email_in_User[0].isd_code,
#                         'mobile': filtered_user_by_user_email_in_User[0].mobile,
#                         'name': filtered_user_by_user_email_in_User[0].username,
#                         'email': filtered_user_by_user_email_in_User[0].email},
#                     'token': token}

#             }
#         if filtered_user_by_user_social_id_in_sociallogin.exists() == False and filtered_user_by_user_email_in_User.exists() == True:
#             username = User.objects.filter(email=email).values('username')[
#                 0].get('username')
#             userid = filtered_user_by_user_email_in_User[0].id
#             Social_Login.objects.create(
#                 user_id=User.objects.get(id=userid),
#                 name=refrensh_name,
#                 email=refrensh_email,
#                 social_id=user_id,
#                 social_type=social_type,
#             )
#             token=tokens(username)
#             device_data(user_id=filtered_user_by_user_email_in_User[0].id, social_type=social_type,
#                         fcm_key=fcm_key, device_type=device_type, ip=ip, device_name=device_name, device_id=device_id,personal_access_token_id=token['access'])
#             return{
#                 "message": "You are logged in successfully",
#                 "data": {
#                     "user": {
#                         'id': filtered_user_by_user_email_in_User[0].id,
#                         'isd_code': filtered_user_by_user_email_in_User[0].isd_code,
#                         'mobile': filtered_user_by_user_email_in_User[0].mobile,
#                         'name': username,
#                         'email': email,
#                         'token': token}}

#             }

#         if filtered_user_by_user_email_in_User.exists() == False and filtered_user_by_user_social_id_in_sociallogin.exists() == False:
#             users = User.objects.create(
#                 email=email,
#                 first_name=name,
#                 username=generate_username(name),
#                 password="random string",
#                 is_verified=True
#             )
#             # users = {
#             #     'email': email,
#             #     'username': generate_username(name),
#             #     'password': "random string"}
#             # user = User.objects.create_user(**users)
#             # user.is_verified = True
#             userid = users.id
#             Social_Login.objects.create(
#                 user_id=User.objects.get(id=userid),
#                 name=refrensh_name,
#                 email=refrensh_email,
#                 social_id=user_id,
#                 social_type=social_type,
#             )
#             token=tokens(users.username)
#             device_data(user_id=userid, social_type=social_type, fcm_key=fcm_key,
#                         device_type=device_type, ip=ip, device_name=device_name, device_id=device_id,personal_access_token_id=token['access'])

#             device_data(user_id=filtered_user_by_user_email_in_User[0].id, social_type=social_type,
#                     fcm_key=fcm_key, device_type=device_type, ip=ip, device_name=device_name, device_id=device_id,personal_access_token_id=token['access'])
#             return{
#                 "message": "You are logged in successfully",
#                 "data": {
#                     "user": {
#                         'id': users.id,
#                         'isd_code': users.isd_code,
#                         'mobile': users.mobile,
#                         'name': users.username,
#                         'email': email},
#                     'token':token }

#             }




def register_social_user(social_id,name,email,social_type, fcm_key, device_type, ip, device_name, device_id,social_data):
    social_id_check=Social_Login.objects.filter(social_id=social_id)
    email_id_check=User.objects.filter(email=email)
    if social_id_check.exists()==True:
        user_id=social_id_check[0].user_id_id
        user=User.objects.get(id=user_id)
        token=tokens(user.email)
        device_data(user_id=user_id, fcm_key=fcm_key, device_type=device_type, ip=ip, device_name=device_name,
         device_id=device_id, social_type=social_type,personal_access_token_id=token['access'])
        is_already_logged_in=False
        if logins.objects.filter(user_id=user_id).count() >1:
            is_already_logged_in=True
        return {
                "message": "You are logged in successfully",
                "data": {
                    "user": {
                        'id': user.id,
                        'isd_code': user.isd_code,
                        'mobile': user.mobile,
                        "mobile_verified_at":user.mobile_verified_at,
                        'name': user.username,
                        'email': user.email},
                        'token': token['access'],
                        'is_already_logged_in':is_already_logged_in}

            }
    if email_id_check.exists()==True and social_id_check.exists()==False:
        user_id=email_id_check[0].id
        user=User.objects.get(id=user_id)
        Social_Login.objects.create(user_id=User.objects.get(id=user_id),social_data=social_data,social_id=social_id,social_type=social_type)
        token=tokens(user.email)
        device_data(user_id, fcm_key, device_type, ip, device_name, device_id, social_type,personal_access_token_id=token['access'])
        is_already_logged_in=False
        if logins.objects.filter(user_id=user_id).count() >1:
            is_already_logged_in=True
        return {
                "message": "You are logged in successfully",
                "data": {
                    "user": {
                        'id': user.id,
                        'isd_code': user.isd_code,
                        'mobile': user.mobile,
                         "mobile_verified_at":user.mobile_verified_at,
                        'name': user.username,
                        'email': user.email},
                        'token': token['access'],
                        'is_already_logged_in':is_already_logged_in}

            }
    if social_id_check.exists()==False and email_id_check.exists()==False:
        user=User.objects.create(email=email,first_name=name,username=generate_username(name),password="random string",email_verified=True,email_verified_at=int(time.time()))
        user_id = user.id
        Social_Login.objects.create(user_id=User.objects.get(id=user_id),social_data=social_data,social_id=social_id,social_type=social_type)
        token=tokens(user.email)
        device_data(user_id=user_id, fcm_key=fcm_key, device_type=device_type, ip=ip, device_name=device_name,
         device_id=device_id, social_type=social_type,personal_access_token_id=token['access'])
        is_already_logged_in=False
        if logins.objects.filter(user_id=user_id).count() >1:
            is_already_logged_in=True
        return {
                "message": "You are logged in successfully",
                "data": {
                    "user": {
                        'id': user.id,
                        'isd_code': user.isd_code,
                        'mobile': user.mobile,
                        "mobile_verified_at":user.mobile_verified_at,
                        'name': user.username,
                        'email': user.email},
                        'token': token['access'],
                        'is_already_logged_in':is_already_logged_in}

            }