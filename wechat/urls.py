from django.urls import path, include


from .views import WechatUserLoginViews, WechatUserUploadViews, wechat_user_list_view


urlpatterns = [

    path('login/', WechatUserLoginViews.as_view(), name='wechat_user_login'),
    path('upload/', WechatUserUploadViews.as_view(), name='wechat_user_upload'),
    path('wechatuserprofile/', wechat_user_list_view, name='wechat_user_list'),
]
