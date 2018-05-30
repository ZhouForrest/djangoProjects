from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from user.models import Users


class UserAuthMiddle(MiddlewareMixin):

    def process_request(self, request):

        ticket = request.COOKIES.get('ticket')
        if not ticket:
            return HttpResponseRedirect(reverse('user:login'))
        user = Users.objects.filter(ticket=ticket).first()
        if not user:
            return render(request, 'login.html')
        request.user = user
