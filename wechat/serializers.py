from rest_framework import serializers
from .models import WechatUserProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class WechatUserSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=100, required=False)
    avatar = serializers.CharField(max_length=200, required=False)

    def update(self, instance, validated_data):
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance

    def create(self, validated_data):
        return WechatUserProfile.objects.create(**validated_data)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    nickname = serializers.CharField(max_length=100, required=False)
    avatar = serializers.CharField(max_length=200, required=False)

    def update(self, instance, validated_data):
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance

    def create(self, validated_data):
        return WechatUserProfile.objects.create(**validated_data)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # 增加想要加到token中的信息
        token['nickname'] = user.nickname
        token['avatar'] = user.avatar
        token['openid'] = user.openid
        return token
