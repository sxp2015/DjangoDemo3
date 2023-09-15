import re
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django_redis import get_redis_connection


# 校验手机格式
def phone_validator(value):
    if not re.match(r"^(1[3|4|5|6|7|8|9])\d{9}$", value):
        raise ValidationError("手机格式错误")


def code_validator(value):
    if not re.match(r"\d{4}$", value):
        raise ValidationError("验证码格式错误")


# 自定义手机号检验规则
class VerifySerializer(serializers.Serializer):
    phone = serializers.CharField(label="手机号", validators=[phone_validator, ])


# 从前台传过来的手机号校验规则
class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(label="手机号", validators=[phone_validator, ])
    code = serializers.CharField(label="短信验证码", validators=[code_validator, ])

    def validated_code(self, value):
        if len(value != 4):
            raise ValidationError("短信格式错误")

        phone = self.initial_data.get('phone')
        conn = get_redis_connection()
        code = conn.get(phone)
        if not code:
            raise ValidationError('验证码过期了')
        if value != code.decode('utf-8'):
            raise ValidationError('验证码格式错误')

        return value
