from rest_framework import generics, status
from requests import Response
from .serializers import ContentPageResponse
from .models import CMS


from Custom.utils import required_header_validate,send_response_validation,headerParam
from Custom.pagination import CustomPagination

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser
from authentication.serializers import *
from drf_spectacular.utils import extend_schema


from Custom.utils import error_422,error_200
from Custom.tag import *

class CMSModleViewSet(generics.GenericAPIView):
    queryset = None
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser,) 
    @extend_schema(
    parameters=headerParam,
    tags=userSetting,
    responses={200:ContentPageResponse, 403:MessageSchema ,401:MessageSchema,422:MessageSchema,500:MessageSchema},
     summary='Get the page content'
    ) 
    def get(self,request,slug,*args, **kwargs):
        headerValidate = required_header_validate(self.request.headers)
        if headerValidate != "valid":
            return error_422(request,message= "header prameter data not valid")
        cms_slug=self.kwargs['slug']
        try:
            cms_slug_obj=CMS.objects.filter(slug=cms_slug)[0].content
        except:
            return error_422(request,message="content not exist for this slug")

        return error_200(request,content=cms_slug_obj)