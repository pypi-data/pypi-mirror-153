from rest_framework_simplejwt.tokens import AccessToken
from Custom.utils import *
url=['/past/logout','/logout','/update-mobile','/update-password','/send-otp','/verify-otp','/update-local']
def simple_middleware(get_response):
    def middleware(request):
        if request.path in url:
            data=(request.headers)
            try:
                tokens = list(data['Authorization'].split(" "))[1]
                access_token_obj = AccessToken(tokens)
            except:
                return error_422(request,message="Invalid Token. You are not authenticated to access this endpoint")
            user_id=access_token_obj['user_id']
            if logins.objects.filter(user_id_id=user_id).filter(personal_access_token_id=access_token_obj).exists()==False:
                return error_422(request, message='you are logged out')
        response = get_response(request)
        return response  

    return middleware
    