from django.conf.urls import include, url
from rest_framework import routers
from .views import AuthRegisterGuest, AuthRegisterHost, GuestInfoView
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'^register_guest/$', AuthRegisterGuest.as_view()),
    url(r'^register_host/$', AuthRegisterHost.as_view()),
    url(r'^login/', obtain_jwt_token),
    url(r'^guest_info/', GuestInfoView.as_view()),
]