from django import forms
from .models import User

class ResetPasswordForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['password']





# import urllib
# class GoogleSocialAuthView(generics.GenericAPIView):

#     serializer_class = GoogleSocialAuthSerializer

#     def post(self, request):
#         """
#         POST with "auth_token"
#         Send an idtoken as from google to get user information
#         """

#         serializer = self.serializer_class(data=request.data)
#         url = "https://www.googleapis.com/plus/v1/people/me?access_token="+request.data['auth_token']
#         print(url)
#         response = urllib.request.urlopen(url)
#         data = json.loads(response.read())
#         print (data)
#         print('token',request.data['auth_token'])
#         serializer.is_valid(raise_exception=True)
#         data = ((serializer.validated_data)['auth_token'])
#         return Response(data, status=status.HTTP_200_OK)