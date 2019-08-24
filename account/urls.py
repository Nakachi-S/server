from django.conf.urls import include, url
from rest_framework import routers
from .views import AuthRegisterGuest, AuthRegisterHost

urlpatterns = [
    url(r'^register_guest/$', AuthRegisterGuest.as_view()),
    url(r'^register_host/$', AuthRegisterHost.as_view()),
]