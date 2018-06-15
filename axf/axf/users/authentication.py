from datetime import datetime

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from app.models import UserTicketModel, UserModel


def is_login(func):
    def check_login(request):
        ticket = request.COOKIES.get('ticket')
        if not ticket:
            return HttpResponseRedirect(reverse('users:login'))
        user_ticket = UserTicketModel.objects.get(ticket=ticket)
        if datetime.utcnow() > user_ticket.out_time.replace(tzinfo=None):
            user_ticket.delete()
            return HttpResponseRedirect(reverse('users:login'))
        user = UserTicketModel.objects.get(ticket=ticket).user
        if not user:
            return HttpResponseRedirect(reverse('users:login'))
        UserTicketModel.objects.filter(Q(user=user_ticket.user) &
                                       ~Q(ticket=ticket)).delete()
        request.user = user_ticket.user
        return func(request)
    return check_login