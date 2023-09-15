import datetime
import os
from config.jwt_config import SIMPLE_JWT as JWT_SETTINGS
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-og7w^tr#0f9wb%!3@3z7f=dujl8_%5qr^0ix=*_5meqns)9n!t'


# 小程序配置信息
APP_ID = 'wx45c6c038a890b402'
APP_SECRET = 'ee4fc7f2d6130170caeb8fa73559e6ad'
JSCODE2SESSION_URL = "https://api.weixin.qq.com/sns/jscode2session"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# 修改LOGO
# SIMPLEUI_LOGO = 'http://p1.lw05.cn/static/index/images/logo.png'
SIMPLEUI_LOGO = 'http://localhost:8000/static/admin/img/logo.png'

# 修改关闭SimpleUI的右侧广告链接
SIMPLEUI_HOME_INFO = False
SIMPLEUI_ANALYSIS = False
# 指定simpleui默认的主题,指定一个文件名，相对路径就从simpleui的theme目录读取
SIMPLEUI_DEFAULT_THEME = 'x-green.css'

# 修改左侧菜单首页设置
SIMPLEUI_HOME_PAGE = '/tasks/dashboard'  # 指向的页面
SIMPLEUI_HOME_TITLE = '首页'
SIMPLEUI_HOME_ICON = 'fas fa-tachometer-alt'
# SIMPLEUI_HOME_ICON = 'fa fa-home'

# 隐藏首页的快捷操作和最近动作
# SIMPLEUI_HOME_QUICK = False
# SIMPLEUI_HOME_ACTION = False


# 开启默认图标，默认为True
# SIMPLEUI_DEFAULT_ICON = False


# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tasks.apps.TasksConfig',
    'home.apps.HomeConfig',
    'api.apps.ApiConfig',
    'utils.apps.UtilsConfig',
    'django_redis',
    'rest_framework',
    'rest_framework_simplejwt',
    # 下面这个app用于刷新refresh_token后，将旧的加到到blacklist时使用
    'rest_framework_simplejwt.token_blacklist',
    'rest_framework.authtoken',
    'wechat.apps.WechatConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'DjangoDemo3.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'DjangoDemo3.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'django_demo3',  # 数据库名
    #     'USER': 'django_demo3',  # 用户名
    #     'PASSWORD': 'aJ28HWYCi5BTGFsS',  # 密码
    #     'HOST': '127.0.0.1',  # 本地ip
    #     'PORT': 3306,  # 端口号
    # }

}
# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# 指定用户模型
AUTH_USER_MODEL = 'wechat.WechatUserProfile'

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

# 指定静态文件的根路径
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = 'static/'
# 添加静态文件路径
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SIMPLEUI_CONFIG = {
    # 是否使用系统默认菜单。
    'system_keep': False,

    # 用于菜单排序和过滤, 不填此字段为默认排序和全部显示。 空列表[] 为全部不显示.
    'menu_display': ['任务管理', '微信管理', '权限认证', '多级菜单测试'],

    # 设置是否开启动态菜单, 默认为False. 如果开启, 则会在每次用户登陆时刷新展示菜单内容。
    # 一般建议关闭。
    'dynamic': False,
    'menus': [
        {
            'app': 'auth',
            'name': '权限认证',
            'icon': 'fas fa-user-shield',
            'models': [
                {
                    'name': '用户列表',
                    'icon': 'fa fa-user',
                    'url': 'auth/user/'
                },
                {
                    'name': '用户组',
                    'icon': 'fa fa-th-list',
                    'url': 'auth/group/'
                }
            ]
        },
        {
            'name': '任务管理',
            'icon': 'fa fa-th-list',
            'models': [
                {
                    'name': '任务列表',
                    # 注意url按'/admin/应用名小写/模型名小写/'命名。
                    'url': '/admin/tasks/task/',
                    'icon': 'fa fa-tasks'
                },
            ]
        },
        {
            'name': '微信管理',
            'icon': 'fa fa-th-list',
            'models': [
                {
                    'name': '用户列表',
                    # 注意url按'/admin/应用名小写/模型名小写/'命名。
                    'url': '/admin/wechat/wechatuser/',
                    'icon': 'fa fa-tasks'
                },
            ]
        },
        {
            # 自2021.02.01+ 支持多级菜单，models 为子菜单名
            'name': '系统管理',
            'icon': 'fa fa-file',
            # 二级菜单
            'models': [{
                'name': '二级菜单',
                'icon': 'far fa-surprise',
                # 第三级菜单 ，
                'models': [
                    {
                        'name': '三级菜单/打开Bing',
                        'url': 'https://cn.bing.com'
                        # 第四级就不支持了，element只支持了3级
                    }, {
                        # 浏览器新标签中打开
                        'newTab': True,
                        'name': '微信公众平台',
                        'icon': 'far fa-surprise',
                        'url': 'https://mp.weixin.qq.com'

                    }
                ]
            }]
        }

    ]}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.IsAdminUser',
        # 'rest_framework.permissions.AllowAny',
        # JWT认证，在前面的认证方案优先
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# 在 setting 配置认证插件的参数
SIMPLE_JWT = JWT_SETTINGS

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}
        }
    }
}
