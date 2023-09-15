from datetime import timedelta

# JWT配置
SECRET_KEY = 'django-insecure-og7w^tr#0f9wb%!3@3z7f=dujl8_%5qr^0ix=*_5meqns)9n!t'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),  # Access Token的有效期
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  # Refresh Token的有效期

    # 对于大部分情况，设置以上两项就可以了，以下为默认配置项目，可根据需要进行调整

    # 是否自动刷新Refresh Token
    'ROTATE_REFRESH_TOKENS': False,
    # 刷新Refresh Token时是否将旧Token加入黑名单，如果设置为False，则旧的刷新令牌仍然可以用于获取新的访问令牌。需要将'rest_framework_simplejwt.token_blacklist
    # '加入到'INSTALLED_APPS'的配置中
    'BLACKLIST_AFTER_ROTATION': False,
    'ALGORITHM': 'HS256',  # 加密算法
    'SIGNING_KEY': SECRET_KEY,  # 签名密匙，这里使用Django的SECRET_KEY

    # 如为True，则在每次使用访问令牌进行身份验证时，更新用户最后登录时间
    "UPDATE_LAST_LOGIN": False,
    # 用于验证JWT签名的密钥返回的内容。可以是字符串形式的密钥，也可以是一个字典。
    "VERIFYING_KEY": "",
    "AUDIENCE": None,  # JWT中的"Audience"声明,用于指定该JWT的预期接收者。
    "ISSUER": None,  # JWT中的"Issuer"声明，用于指定该JWT的发行者。
    "JSON_ENCODER": None,  # 用于序列化JWT负载的JSON编码器。默认为Django的JSON编码器。
    "JWK_URL": None,  # 包含公钥的URL，用于验证JWT签名。
    "LEEWAY": 0,  # 允许的时钟偏差量，以秒为单位。用于在验证JWT的过期时间和生效时间时考虑时钟偏差。

    # 用于指定JWT在HTTP请求头中使用的身份验证方案。默认为"Bearer"
    "AUTH_HEADER_TYPES": ("Bearer",),
    # 包含JWT的HTTP请求头的名称。默认为"HTTP_AUTHORIZATION"
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    # 用户模型中用作用户ID的字段。默认为"id"。
    "USER_ID_FIELD": "id",
    # JWT负载中包含用户ID的声明。默认为"user_id"。
    "USER_ID_CLAIM": "user_id",

    # 用于指定用户身份验证规则的函数或方法。默认使用Django的默认身份验证方法进行身份验证。
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    #  用于指定可以使用的令牌类。默认为"rest_framework_simplejwt.tokens.AccessToken"。
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    # JWT负载中包含令牌类型的声明。默认为"token_type"。
    "TOKEN_TYPE_CLAIM": "token_type",
    # 用于指定可以使用的用户模型类。默认为"rest_framework_simplejwt.models.TokenUser"。
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    # JWT负载中包含JWT ID的声明。默认为"jti"。
    "JTI_CLAIM": "jti",

    # 在使用滑动令牌时，JWT负载中包含刷新令牌过期时间的声明。默认为"refresh_exp"。
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    # 滑动令牌的生命周期。默认为5分钟。
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    # 滑动令牌可以用于刷新的时间段。默认为1天。
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    # 用于生成访问令牌和刷新令牌的序列化器。
    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    # 用于刷新访问令牌的序列化器。默认
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    # 用于验证令牌的序列化器。
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    # 用于列出或撤销已失效JWT的序列化器。
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    # 用于生成滑动令牌的序列化器。
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    # 用于刷新滑动令牌的序列化器。
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}
