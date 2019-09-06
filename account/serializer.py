from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers

from .models import User, UserManager, Guest_info


class AccountSerializerGuest(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'email', 'password')

    def create(self, validated_data):
        return User.objects.create_user_guest(request_data=validated_data)

class AccountSerializerHost(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'email', 'password')

    def create(self, validated_data):
        return User.objects.create_user_host(request_data=validated_data)

class GuestInfoSerializer(serializers.ModelSerializer):
    # SerializerMethodField は get_xxxx ってなっているメソッドをコールする
    # full_name = serializers.SerializerMethodField()

    class Meta:
        model = Guest_info
        fields = ('user_id', 'country', 'address', 'birth_day', 'gender', 'qr_code')
        read_only_fields = ('user_id',)


    def create(self, validated_data):
        guest_info = Guest_info(
            country=validated_data['country'],
            address=validated_data['address'],
            birth_day=validated_data['birth_day'],
            gender=validated_data['gender']
        )

        guest_info.save()
        return guest_info