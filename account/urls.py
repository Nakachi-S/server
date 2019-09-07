from django.urls import path, include  # includeを追加
from rest_framework import routers
from .views import AuthRegisterGuest, AuthRegisterHost, GuestInfoPost, GuestInfoGet, HostInfoPost, HostInfoGet
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('register_guest/', AuthRegisterGuest.as_view()),
    path('register_host/', AuthRegisterHost.as_view()),
    path('login/', obtain_jwt_token),
    path('guest_info_post/', GuestInfoPost.as_view()),
    path('guest_info_get/<int:pk>/', GuestInfoGet.as_view()),
    path('host_info_post/', HostInfoPost.as_view()),
    path('host_info_get/<int:pk>', HostInfoGet.as_view()),
]