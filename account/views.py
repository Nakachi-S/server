from django.contrib.auth import authenticate
from rest_framework import authentication, permissions, generics
from rest_framework_jwt.settings import api_settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from django.db import transaction
from django.http import HttpResponse, Http404

from rest_framework import status, viewsets, filters
from rest_framework.views import APIView

from .serializer import AccountSerializerGuest, AccountSerializerHost, GuestInfoSerializer, HostInfoSerializer
from .models import User, UserManager, Guest_info


# ユーザ情報取得のView(GET)
class AuthInfoGetView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = AccountSerializerGuest

    def get(self, request, format=None):
        return Response(data={
            # 'username': request.user.username,
            'email': request.user.email,
            },
            status=status.HTTP_200_OK)

# ゲストユーザ作成のView(POST)
class AuthRegisterGuest(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = AccountSerializerGuest

    @transaction.atomic
    def post(self, request, format=None):
        serializer = AccountSerializerGuest(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ホストユーザ作成のView(POST)
class AuthRegisterHost(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = AccountSerializerHost

    @transaction.atomic
    def post(self, request, format=None):
        serializer = AccountSerializerHost(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
# ゲストユーザの宿泊台帳(POST)
class GuestInfoPost(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Guest_info.objects.all()
    serializer_class = GuestInfoSerializer
    
    def post(self, request, format=None):
        serializer = GuestInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ゲストユーザの宿泊台帳(GET)
class GuestInfoGet(generics.RetrieveAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Guest_info.objects.all()
    # lookup_field = 'user_id'
    serializer_class = GuestInfoSerializer



# ホストユーザの情報(POST)
class HostInfoPost(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Guest_info.objects.all()
    serializer_class = HostInfoSerializer
    
    def post(self, request, format=None):
        serializer = HostInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ホストユーザの情報(GET)
class HostInfoGet(generics.RetrieveAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Guest_info.objects.all()
    # lookup_field = 'user_id'
    serializer_class = HostInfoSerializer