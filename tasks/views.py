from django.shortcuts import render
from django.contrib.auth.models import User
from wechat.models import WechatUserProfile
from django.http.response import HttpResponse

from DjangoDemo3.settings import BASE_DIR
from tasks.models import Task
from django.views.generic import View


# Create your views here.

def dashboard(request):
    user_count = WechatUserProfile.objects.count()
    task_count = Task.objects.count()
    context = {'user_count': user_count, 'task_count': task_count}
    return render(request, 'tasks/dashboard.html', context)
    # return HttpResponse("hello")
