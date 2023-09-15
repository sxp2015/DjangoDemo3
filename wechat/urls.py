from django.urls import path, include
from .views import WechatUserLoginViews, WechatUserUploadViews

# router = routers.DefaultRouter()
# router.register(r'wechat_users', WechatUserLoginViews, basename='wechat_users')

urlpatterns = [
    # path('', include(router.urls)),
    path('login/', WechatUserLoginViews.as_view(), name='wechat_user_login'),
    path('upload/', WechatUserUploadViews.as_view(), name='wechat_user_upload'),
]
