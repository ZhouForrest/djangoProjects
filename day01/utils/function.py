from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from user.models import Users


def is_login(func):
    def check_login(request):
        path = request.path
        ticket = request.COOKIES.get('ticket')
        if not ticket:
            return HttpResponseRedirect(reverse('user:login'))
        user = Users.objects.filter(ticket=ticket).first()
        if not user:
            return render(request, 'login.html')
        request.user = user
        return func(request)
    return check_login