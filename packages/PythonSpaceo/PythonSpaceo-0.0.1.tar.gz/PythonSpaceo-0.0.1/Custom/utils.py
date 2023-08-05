from django.http import JsonResponse
import hmac
import hashlib
from django.http import JsonResponse
from rest_framework import status

from authentication.models import User,logins

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from django.utils import translation



headerParam2=[
        OpenApiParameter(
            name='Accept', location=OpenApiParameter.HEADER,
            type=OpenApiTypes.STR,
            description='Type of response you are expecting from API. i.e. (application/json)',
            required=True,
            default='application/json',
        ),
    ]


headerParam = [
        OpenApiParameter(
            name='Accept-Language', location=OpenApiParameter.HEADER,
            type=OpenApiTypes.STR,
            description='ISO 2 Letter Language Code',
            required=True,
            enum=['en', 'ar'],
            default='en',
        ),
        OpenApiParameter(
            name='Accept', location=OpenApiParameter.HEADER,
            type=OpenApiTypes.STR,
            description='Type of response you are expecting from API. i.e. (application/json)',
            required=True,
            default='application/json',
        ),
    ]



headerParam3 = [
        OpenApiParameter(
            name='Accept-Language', location=OpenApiParameter.HEADER,
            type=OpenApiTypes.STR,
            description='ISO 2 Letter Language Code',
            required=True,
            enum=['en', 'ar'],
            default='en',
        ),
        OpenApiParameter(
            name='Accept', location=OpenApiParameter.HEADER,
            type=OpenApiTypes.STR,
            description='Type of response you are expecting from API. i.e. (application/json)',
            required=True,
            default='application/json',
        ),
        OpenApiParameter(
            name='plateform', location=OpenApiParameter.HEADER,
            type=OpenApiTypes.STR,
            description='Plateform of which you want version information. (ios & android)',
            required=True,
            enum=['android', 'ios'],
            default='ios',
        ),
    ]

def required_header_validate(headerData):

        if "Accept-Language" not in headerData:
            return _("Language filed is required")

        translation.activate(headerData["Accept-Language"])
        return ("valid")

def send_response_validation(request, code, message):

    response = JsonResponse(data={'responseCode': code, 'responseMessage': message})
    response.status_code = 200
    return response

def error_404(request, code, message):

    response = JsonResponse(data={'responseCode': code, 'responseMessage': message})
    response.status_code = 404
    return response

def error_500(request, code, message):
    message = 'An internal error occurred. An administrator has been notified. '
    
    response = JsonResponse(data={'responseCode': code, 'responseMessage': message})
    response.status_code = 500
    return response

def error_400(request, message):

    response = JsonResponse(data={'Message': message})
    response.status_code = 400
    return response

def correct_200(request, message):

    response = JsonResponse(data={'message': message})
    response.status_code = 200
    return response


def error_200(request, content):
    data={
        'content':content
    }
    response = JsonResponse(data={'message':'ok','data':data})
    response.status_code = 200
    return response 

def error_401(request, message):

    response = JsonResponse(data={'message': message})
    response.status_code = 401
    return response

def error_422(request, message):

    response = JsonResponse(data={'message': message})
    response.status_code = 422
    return response

def success_response(request,code, message,data):
    response = JsonResponse(data={'responseCode': code, 'responseMessage': message,'candidate_uuid': str(data)})
    response.status_code = 200
    return response


def tokens(email):
    user = User.objects.get(email=email)

    return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        } 

from django.core.mail import EmailMessage,send_mail


@staticmethod
def send_email(data):
    print(data)
    print(data['email_subject'],data['email_body'],data['from_email'],[data['recipient']])
    email = EmailMessage(subject=data['email_subject'],body=data['email_body'],to=[data['recipient']],from_email=data['from_email'])
    email.send()



