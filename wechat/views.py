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
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from PIL import Image
from rest_framework.decorators import api_view
from DjangoDemo3 import settings
from .models import WechatUserProfile
from rest_framework.views import APIView
from django.core.files.storage import FileSystemStorage, default_storage
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, Token
from .serializers import WechatUserSerializer, MyTokenObtainPairSerializer


# 处理小程序用户登陆的View
class WechatUserLoginViews(APIView):
    # authentication_classes = []
    # authentication_classes = [SessionAuthentication]
    permission_classes = []
    """ 获取openid存储用户信息"""

    # 微信登陆认证
    def post(self, request):
        # 获取到前端回传过来的code
        data = json.loads(request.body)
        # code 有效期5分钟
        code = data.get('code')
        nickname = data.get('nickName', '')
        avatar = data.get('avatarUrl', '')

        print('avatar:', avatar)

        if not code:
            return Response({'error': 'Missing code parameter'}, status=status.HTTP_400_BAD_REQUEST)

        # 构造向微信发送请求的url
        url = f"{settings.JSCODE2SESSION_URL}?appid={settings.APP_ID}&secret={settings.APP_SECRET}&js_code={code}&grant_type=authorization_code"

        try:
            # 向微信服务器发起 get 请求
            response = requests.get(url)
            response_data = response.json()
            # 这里就是拿到的 openid 和 session_key
            openid = response_data.get('openid')
            # print('openid:', openid)
            session_key = response_data.get('session_key')
            print('session_key:', session_key)
            # 如果没有openID返回提示给前端
            if not openid:
                return Response({'error': 'Failed to obtain openid'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                print('openid:', openid)
            # 查询或创建微信用户
            defaults = {'username': openid, 'password': openid}
            if nickname:
                defaults['nickname'] = nickname
            if avatar:
                defaults['avatar'] = avatar

            # 通过openid更新或创建用户
            wechat_user, created = WechatUserProfile.objects.update_or_create(
                openid=openid,
                defaults=defaults,
            )
            # 生成token
            token = str(RefreshToken.for_user(wechat_user).access_token)

            # 返回用户信息
            serializer = WechatUserSerializer(data={
                'nickname': wechat_user.nickname if wechat_user.nickname else '微信用户',
                'avatar': wechat_user.avatar if wechat_user.avatar else None,
                'openid': wechat_user.openid if wechat_user.openid else None,
                'token': token if token else None
            })
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except requests.RequestException:
            return Response({'error': 'Failed to connect to WeChat server'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 已经完成登陆，请求其他数据时的View
    def get(self, request):

        openid = request.user.openid
        wechat_user = WechatUserProfile.objects.filter(openid=openid).first()

        if not wechat_user:
            return Response({'error': 'WeChat user not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = WechatUserSerializer(data={
            'nickname': wechat_user.nickname,
            'avatar': wechat_user.avatar
        })
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 处理微信小程序上传的用户头像保存到服务器
class WechatUserUploadViews(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        # 判断上传图片的用户是否携带token 或者，是已经完成认证的用户

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
