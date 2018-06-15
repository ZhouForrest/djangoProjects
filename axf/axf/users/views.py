from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from app.models import UserModel, UserTicketModel
from utils.function import get_ticket


def login(request):

    if request.method == 'GET':
        return render(request, 'user/user_login.html')

    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = UserModel.objects.filter(username=username).first()

        if user:
            if check_password(password, user.password):
                ticket = get_ticket()
                #保存在客户端
                response = HttpResponseRedirect(reverse('axf:mine'))
                out_time = datetime.now() + timedelta(days=1)
                response.set_cookie('ticket', ticket, expires='out_time')
                #保存在服务端
                UserTicketModel.objects.create(user=user, ticket=ticket, out_time=out_time)
                return response
            else:
                msg = '用户名或密码错误'
                return render(request, 'user/user_login.html', {'msg': msg})
        else:
            msg = '用户不存在'
            return render(request, 'user/user_login.html', {'msg': msg})


def register(request):

    if request.method == 'GET':
        return render(request, 'user/user_register.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        pwd = make_password(request.POST.get('password'))
        email = request.POST.get('email')
        icon = request.FILES.get('icon')
        if not all([username, pwd, email, icon]):
            msg = '用户信息不能为空'
            return render(request, 'user/user_register.html', {'msg': msg})
        UserModel.objects.create(username=username, password=pwd, icon=icon, eamil=email)
        return HttpResponseRedirect(reverse('users:login'))


def logout(request):

    if request.method == 'GET':
        response = HttpResponseRedirect(reverse('users:login'))
        response.delete_cookie('ticket')
        return response

