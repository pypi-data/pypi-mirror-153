from django.urls import path
from .views import *

urlpatterns = [
    # path('', CMSModleViewSet.as_view()),
    path('<str:slug>', CMSModleViewSet.as_view(), name='cms'),
]