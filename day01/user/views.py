import random

from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from user.models import Users


# def register(request):
#
#     if request.method == 'GET':
#
#         return render(request, 'register.html')
#
#     else:
#         username = request.POST.get('username')
#         pwd1 = request.POST.get('pwd1')
#         pwd2 = request.POST.get('pwd2')
#         if not all([username, pwd1, pwd2]):
#             msg = '请输入完整信息'
#             return render(request, 'register.html', {'msg': msg})
#         elif pwd1 != pwd2:
#             msg = '密码不一致'
#             return render(request, 'register.html', {'msg': msg})
#         else:
#             User.objects.create_user(username=username, password=pwd1)
#             return HttpResponseRedirect(reverse('user:login'))


# def login(request):
#
#     if request.method == 'GET':
#         return render(request, 'login.html')
#
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         pwd = request.POST.get('pwd')
#         #验证用户信息
#         user = auth.authenticate(username=username, password=pwd)
#         if user:
#             auth.login(request, user)
#             return HttpResponseRedirect(reverse('app:index'))
#         else:
#             msg = '用户名或密码错误'
#             return render(request, 'login.html', {'msg':msg})
#
#
# def logout(request):
#     if request.method == 'GET':
#         auth.logout(request)
#         return HttpResponseRedirect(reverse('user:login'))
#
#
from utils.function import is_login


def register(request):

    if request.method == 'GET':

        return render(request, 'register.html')

    else:
        username = request.POST.get('username')
        pwd1 = request.POST.get('pwd1')
        pwd2 = request.POST.get('pwd2')
        if not all([username, pwd1, pwd2]):#判断是否存在空值
            msg = '请输入完整信息'
            return render(request, 'register.html', {'msg': msg})
        elif pwd1 != pwd2:
            msg = '密码不一致'
            return render(request, 'register.html', {'msg': msg})
        else:
            Users.objects.create(username=username, password=pwd1)
            return HttpResponseRedirect(reverse('user:login'))


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')
        #验证用户信息
        user = Users.objects.filter(username=username, password=pwd).first()
        if user:
            str = 'qwertyuiopa123456sdfghjklzxcvbnm,./1234567890-'
            ticket = ''
            for _ in range(28):
                ticket += random.choice(str)
            #保存在服务端
            user.ticket = ticket
            user.save()
            #保存在客户端 cookie
            response = HttpResponseRedirect(reverse('app:index'))
            response.set_cookie('ticket', ticket)
            return response
        else:
            msg = '用户名或密码错误'
            return render(request, 'login.html', {'msg': msg})


def logout(request):
    response = HttpResponseRedirect(reverse('user:login'))
    response.delete_cookie('ticket')
    return response


# def userper(request):
#
#     user = Users.objects.filter(username='张飞').first()
#     permission = user.role.r_p.all()#查看所有权限
#     permission.filter(p_en='STULIST').exists()#查看是否存在每=某个权限
#     return HttpResponseRedirect(reverse('app:index'))
