from rest_framework import serializers

class CmsRequest(serializers.Serializer):
    cms_slug=serializers.CharField()

class Content(serializers.Serializer):
    content=serializers.CharField()

class ContentPageResponse(serializers.Serializer):
    message=serializers.CharField(required=True)
    data=Content()
    


