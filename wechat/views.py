import datetime
import json
import io
import os
import time
import uuid
import requests
from urllib.parse import urljoin

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from DjangoDemo3 import settings
from .models import WechatUserProfile
from rest_framework.views import APIView
from django.core.files.storage import FileSystemStorage, default_storage
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, Token
from .serializers import WechatUserProfileListSerializer, WechatUserProfileUpdateOrCreateSerializer, \
    MyTokenObtainPairSerializer

# 定义默认头像
DEFAULT_AVATAR = "https://mmbiz.qpic.cn/mmbiz/icTdbqWNOwNRna42FI242Lcia07jQodd2FJGIYQfG0LAJGFxM4FbnQP6yfMxBgJ0F3YRqJCJ1aPAK2dQagdusBZg/0"
# 定义默认昵称
DEFAULT_NICKNAME = "微信用户"


# 处理小程序用户登陆的View
class WechatUserLoginViews(APIView):
    """ 处理小程序登陆并存储用户信息"""

    # 权限控制
    permission_classes = []

    @staticmethod
    def request_wechat_server(code):
        url = f"{settings.JSCODE2SESSION_URL}?appid={settings.APP_ID}&secret={settings.APP_SECRET}&js_code={code}&grant_type=authorization_code"
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        return response.json()

    # 微信登陆认证
    def post(self, request):
        # 获取到前端回传过来的code
        # code 有效期5分钟
        code = request.data.get('code')
        nickname = request.data.get('nickname', '')
        avatar = request.data.get('avatar', '')
        # 构造向微信发送请求的url
        url = f"{settings.JSCODE2SESSION_URL}?appid={settings.APP_ID}&secret={settings.APP_SECRET}&js_code={code}&grant_type=authorization_code"

        if not code:
            return Response({'error': 'Missing code parameter'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 调用类方法，向微信服务器发起 get 请求
            response_data = self.request_wechat_server(code)
            # 这里就是拿到的 openid 和 session_key
            openid = response_data.get('openid')
            # print('openid:', openid)
            session_key = response_data.get('session_key')
            print('session_key:', session_key)
            # 如果没有openID返回提示给前端
            if not openid:
                return Response({'error': 'Failed to obtain openid'}, status=status.HTTP_400_BAD_REQUEST)

            # 整理保存用户的数据
            defaults = {'username': openid, 'password': openid, 'nickname': nickname if nickname else DEFAULT_NICKNAME,
                        'avatar': avatar if avatar else DEFAULT_AVATAR}

            # 通过openid更新或创建用户
            wechat_user, created = WechatUserProfile.objects.update_or_create(
                openid=openid,
                defaults=defaults,
            )
            # 生成token
            token = str(RefreshToken.for_user(wechat_user).access_token)

            # 序列化返回给用户的数据
            serializer_data = {
                'nickname': wechat_user.nickname or DEFAULT_NICKNAME,
                'avatar': wechat_user.avatar or DEFAULT_AVATAR,
                'openid': wechat_user.openid,
                'token': token
            }

            # 数据校验并返回用户信息
            serializer = WechatUserProfileUpdateOrCreateSerializer(data=serializer_data)
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

        serializer = WechatUserProfileUpdateOrCreateSerializer(data={
            'openid': wechat_user.openid,
            'token': wechat_user.token,
            'nickname': wechat_user.nickname,
            'avatar': wechat_user.avatar
        })
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 处理微信小程序上传的用户头像保存到服务器
class WechatUserUploadViews(APIView):
    permission_classes = [IsAuthenticated]

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


# 返回所有微信用户的列表View
def wechat_user_list_view(request):
    queryset = WechatUserProfile.objects.all()
    template = loader.get_template('wechat/wechat_user_list.html')
    context = {
        'user_list': queryset,
    }
    rendered_html = template.render(context, request)
    return HttpResponse(rendered_html)

