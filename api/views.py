import uuid

from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import UserInfo
from api.serializer.login_serializer import LoginSerializer, VerifySerializer
from utils.sendSMS import TencentSMS


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        # 调用自定义校验类，校验传过来的值
        ser = LoginSerializer(data=request.data)
        if not ser.is_valid():
            return Response({"status": False, "message": "验证码错误"})
        # 获取校验成功的手机号，去查询数据库是否存在用户
        phone = ser.validated_data.get('phone')
        user = UserInfo.objects.filter(phone=phone).first()

        # 先查询用户是否存在，新用户则isNewUser=True,否则为False
        user, isNewUser = UserInfo.objects.get_or_create(phone=phone)
        # 重新生成Token，赋值给用户并保存
        user.token = str(uuid.uuid4())
        user.save()
        print(isNewUser, user)
        # 整理数据返回
        return Response({"status": True, "data": {"token": user.token, "phone": phone}})


class SmsView(APIView):
    def get(self, request, *args, **kwargs):
        # 获取手机号
        ser = VerifySerializer(data=request.query_params)
        if not ser.is_valid():
            return Response({"status": False, "message": "手机格式错误"})
        phone = ser.validated_data.get('phone')

        print(phone)
        tencentSMS = TencentSMS()
        tencentSMS.send_sms([phone, ])

        return Response({"status": "手机号正确", "message": "发送成功"})
