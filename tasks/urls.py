from django.urls import path, include
from rest_framework import routers
from tasks import views

# router = routers.DefaultRouter()
# router.register(r'dashboard', dashboard, basename='dashboard')

urlpatterns = [
    # path('', include(router.urls)),
    path('dashboard/', views.dashboard, name='dashboard'),
]
