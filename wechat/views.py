import datetime
import json
import io
import os
import time
import uuid
import requests
from urllib.parse import urljoin
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from PIL import Image
from rest_framework.decorators import api_view
from DjangoDemo3 import settings
from .models import WechatUserProfile
from rest_framework.views import APIView
from django.core.files.storage import FileSystemStorage, default_storage
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import WechatUserSerializer, MyTokenObtainPairSerializer


# 处理小程序用户登陆的View
class WechatUserLoginViews(APIView):
    """ 获取opeid存储用户信息"""
    # 微信登陆认证
    def post(self, request):
        # 获取到前端回传过来的code
        code = json.loads(request.body).get('code')  # 这个code有效期为5分钟
        nickname = json.loads(request.body).get('nickName', '')
        avatar = json.loads(request.body).get('avatarUrl', '')
        # 构造向微信发送请求的url
        url = f"{settings.JSCODE2SESSION_URL}?appid={settings.APP_ID}&secret={settings.APP_SECRET}&js_code={code}&grant_type=authorization_code"

        try:
            # 向微信服务器发起 get 请求
            response = requests.get(url)
            # 这里就是拿到的 openid 和 session_key
            openid = response.json()['openid']
            session_key = response.json()['session_key']
            # 查询或创建微信用户
            defaults = {'username': openid}
            if nickname:
                defaults['nickname'] = nickname
            if avatar:
                defaults['avatar'] = avatar

            # 通过openid更新或创建用户
            wechat_user, created = WechatUserProfile.objects.update_or_create(
                openid=openid,
                defaults=defaults
            )
            # 返回用户信息
            serializer = WechatUserSerializer(data={
                'nickname': wechat_user.nickname if wechat_user.nickname else '微信用户',
                'avatar': wechat_user.avatar if wechat_user.avatar else None
            })
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except KeyError:
            return Response({'code': 'fail'})

    def get(self, request):
        openid = json.loads(request.body).get('openid', '')
        wechat_user = WechatUserProfile.objects.filter(openid=openid)
        serializer = WechatUserSerializer(data={
            'nickname': wechat_user.nickname,
            'avatar': wechat_user.avatar
        })
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 处理微信小程序上传的用户头像保存到服务器
class WechatUserUploadViews(APIView):

    def post(self, request):
        avatar_file = request.FILES.get('avatar_file')

        # 生成唯一的文件名
        file_extension = avatar_file.name.split('.')[-1]
        filename = f'{uuid.uuid4().hex}.{file_extension}'

        # 定义头像文件保存到的目录（按日期创建）
        avatar_file_path = os.path.join(settings.MEDIA_ROOT, 'images', 'avatar',
                                        datetime.datetime.now().strftime('%Y%m%d'))

        # 如果目录不存在，则新建目录
        if not os.path.exists(avatar_file_path):
            os.makedirs(avatar_file_path)
        file_path = os.path.join(avatar_file_path, filename)

        # 保存文件
        with default_storage.open(file_path, 'wb+') as destination:
            for chunk in avatar_file.chunks():
                destination.write(chunk)

                # 生成文件的相对路径
                relative_file_path = os.path.join(settings.MEDIA_URL, 'images', 'avatar',
                                                  datetime.datetime.now().strftime('%Y%m%d'),
                                                  filename)
                # 生成绝对路径 build_absolute_uri 方法接受一个相对路径作为参数，并根据当前请求的协议、主机和端口信息，以及传入的相对路径，生成完整的绝对 URL。
                absolute_file_path = urljoin(request.build_absolute_uri(reverse('wechat_user_upload')),
                                             relative_file_path).replace('\\', '/').replace('wechat/upload/', '')
        # 返回头像地址
        return Response({'code': 'success', 'file_path': absolute_file_path})


class MyObtainTokenPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
