from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from app import views

route = SimpleRouter()
route.register(r'^api/cart', views.Api_cartmodel)
urlpatterns = [
    url(r'^home/', views.home, name='home'),
    url(r'^mine/', views.mine, name='mine'),
    url(r'^market/$', views.market, name='market'),
    url(r'^market/(\d+)/(\d+)/(\d+)', views.market_params, name='market_params'),
    url(r'^addcart/', views.addcart, name='addcart'),
    url(r'^subcart/', views.subcart, name='subcart'),
    url(r'^cart/', views.cart, name='cart'),
    url(r'^change_cart_select/', views.change_cart_select, name='change_cart_select'),
    url(r'^total/', views.total, name='total'),
    url(r'^all_select/', views.all_select, name='all_select'),
    url(r'^order/', views.order, name='order'),
    url(r'^order_list/', views.order_list, name='order_list'),
    url(r'^alipy/', views.alipy, name='alipy'),
    url(r'^order_payed/',views.order_payed, name='order_payed'),
    url(r'^wait_pay_to_payed/', views.wait_pay_to_payed, name='wait_pay_to_payed'),
    url(r'^receipt', views.receipt, name='receipt')
]
urlpatterns += route.urls