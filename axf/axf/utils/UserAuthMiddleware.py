from datetime import datetime

from django.db.models import Q
from django.http import HttpResponseRedirect

from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from app.models import UserTicketModel, UserModel


class UserMiddle(MiddlewareMixin):

    def process_request(self, request):
        need_login = ['axf/mine']
        if request.path in need_login:
            ticket = request.COOKIES.get('ticket')
            if not ticket:
                return HttpResponseRedirect(reverse('users:login'))
            user_ticket = UserTicketModel.objects.filter(ticket=ticket).first()
            if datetime.utcnow() > user_ticket.out_time.replace(tzinfo=None):
                user_ticket.delete()
                return HttpResponseRedirect(reverse('users:login'))
            else:
                UserTicketModel.objects.filter(Q(user=user_ticket.user) &
                                               ~Q(ticket=ticket)).delete()
                request.user = user_ticket.user
        else:
            return None


