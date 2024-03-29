from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers

from .models import User, UserManager, Guest_info, Host_info
import random, string


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

# ログイン情報取得用
class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'email', 'is_info', 'is_host')

# 宿泊台帳用
class GuestInfoSerializer(serializers.ModelSerializer):
    # SerializerMethodField は get_xxxx ってなっているメソッドをコールする
    # full_name = serializers.SerializerMethodField()

    class Meta:
        model = Guest_info
        fields = ('user', 'country', 'address', 'birth_day', 'gender')


    def create(self, validated_data):
        # print(validated_data['user'].id)
        guest_info = Guest_info(
            user=User.objects.get(pk=validated_data['user'].id),
            country=validated_data['country'],
            address=validated_data['address'],
            birth_day=validated_data['birth_day'],
            gender=validated_data['gender'],
        )
        
        guest_info.save()
        
        # userテーブルのis_infoをTrueにする
        # print(validated_data['user'].id)
        tmp = User.objects.get(pk=validated_data['user'].id)
        tmp.is_info = True
        tmp.save()
        
        return guest_info
    
# ホストユーザの情報
class HostInfoSerializer(serializers.ModelSerializer):
    # SerializerMethodField は get_xxxx ってなっているメソッドをコールする
    # full_name = serializers.SerializerMethodField()

    class Meta:
        model = Host_info
        fields = ('user', 'hotel_name', 'phone', 'address', 'qr_code')
        read_only_fields = ('qr_code',)


    def create(self, validated_data):
        # print(validated_data['user'].id)
        host_info = Host_info(
            user=User.objects.get(pk=validated_data['user'].id),
            hotel_name=validated_data['hotel_name'],
            phone=validated_data['phone'],
            address=validated_data['address'],
            qr_code=randomstring(200),
        )

        host_info.save()
        
        # userテーブルのis_infoをTrueにする
        # print(validated_data['user'].id)
        tmp = User.objects.get(pk=validated_data['user'].id)
        tmp.is_info = True
        tmp.save()
        
        return host_info


# ランダムな文字列を生成するための関数
def randomstring(n):
   return ''.join(random.choices(string.ascii_letters + string.digits, k=n))