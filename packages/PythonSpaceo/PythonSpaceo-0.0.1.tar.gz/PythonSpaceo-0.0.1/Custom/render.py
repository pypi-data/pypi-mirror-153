from django.http import HttpResponse
from rest_framework import renderers
import json
from rest_framework import status

class UserRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''
        if "Authentication credentials were not provided" in str(data):
            response = json.dumps({ 'message':'Invalid Token. You are not authenticated to access this endpoint'})
            
        else:
            response = json.dumps({
                    
                    'message': "Invalid Token. You are not authenticated to access this endpoint",
                    # 'responseMessage': data['detail']
                })
        return response
