from rest_framework import serializers
from .models import WechatUserProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class WechatUserSerializer(serializers.Serializer):
    openid = serializers.CharField(max_length=50, required=True)
    nickname = serializers.CharField(max_length=100, required=False)
    avatar = serializers.CharField(max_length=255, required=False)
    token = serializers.CharField(max_length=255, required=True)

    def update(self, instance, validated_data):
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.openid = validated_data.get('openid', instance.openid)
        instance.token = validated_data.get('token', instance.token)
        instance.save()
        return instance

    def create(self, validated_data):
        return WechatUserProfile.objects.create(**validated_data)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    openid = serializers.CharField(max_length=50, required=True)

    def update(self, instance, validated_data):
        instance.openid = validated_data.get('openid', instance.openid)
        instance.save()
        return instance

    def create(self, validated_data):
        return WechatUserProfile.objects.create(**validated_data)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # 增加想要加到token中的信息
        token['openid'] = user.openid
        return token
