from django.urls import path

from api.views import LoginView, SmsView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from wechat.views import MyObtainTokenPairView
urlpatterns = [
    path('login/', LoginView.as_view()),
    path('sms/', SmsView.as_view()),

    path('token/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 下面这个是用来验证token的，根据需要进行配置
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]
