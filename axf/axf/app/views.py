from rest_framework import mixins, viewsets
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from app.cartSeariliazer import SerializerCart
from app.models import MainWheel, MainNav, MainShop, MustBuy, MainShow, FoodType, Goods, CartModel, OrderModel, \
    OrderGoodsModel
from users.authentication import is_login
from utils.function import get_ticket


def home(request):

    if request.method == 'GET':
        mainwheels = MainWheel.objects.all()
        navs = MainNav.objects.all()
        shops = MainShop.objects.all()
        buys = MustBuy.objects.all()
        shows = MainShow.objects.all()
        types = FoodType.objects.all()
        goods = Goods.objects.all()
        data = {
            'title': '首页',
            'mainwheels': mainwheels,
            'navs': navs,
            'shops': shops,
            'buys': buys,
            'shows': shows,
            'types': types,
            'goods': goods
        }
        return render(request, 'home/home.html', data)

# @is_login

@is_login
def mine(request):
    if request.method == 'GET':
        user = request.user
        wait_pay = OrderModel.objects.filter(user_id=user.id, o_status=0).count()
        payed = OrderModel.objects.filter(user_id=user.id, o_status=1).count()
        return render(request, 'mine/mine.html', {'wait_pay': wait_pay, 'payed': payed})


def market(request):
    if request.method == 'GET':

        return HttpResponseRedirect(reverse('axf:market_params', args=('104749', '0', '0')))


def market_params(request, typeid, cid, sid):
    if request.method == 'GET':
        foodtypes = FoodType.objects.all()
        if cid == '0':
            goods = Goods.objects.filter(categoryid=typeid)
        else:
            goods = Goods.objects.filter(categoryid=typeid,
                                         childcid=cid)
        foodtypes_current = FoodType.objects.filter(typeid=typeid).first()
        if foodtypes_current:
            childtypenames = foodtypes_current.childtypenames.split('#')
            child_list = []
            for childtypename in childtypenames:
                child = childtypename.split(':')
                child_list.append(child)
            if sid == '0':
                pass
            if sid == '1':
                goods = goods.order_by('productnum')
            if sid == '2':
                goods = goods.order_by('-price')
            if sid == '3':
                goods = goods.order_by('price')

            data = {
                'foodtypes': foodtypes,
                'goods': goods,
                'typeid': typeid,
                'child_list': child_list,
                'cid': cid
                }
            return render(request, 'market/market.html', data)

@is_login
def addcart(request):
    data = {}
    if request.method == 'POST':
        goods_id = request.POST.get('goods_id')
        user = request.user
        if user.id:
            data = {
                'code': 200,
                'msg': '请求成功'
            }
            user_cart = CartModel.objects.filter(user=user, goods_id=goods_id).first()
            if user_cart:
                user_cart.c_num += 1
                user_cart.is_select = True
                user_cart.save()
                data['c_num'] = user_cart.c_num
            else:
                user_cart = CartModel.objects.create(user=user, goods_id=goods_id)
                data['c_num'] = 1
            return JsonResponse(data)
        data['msg'] = '未登录,请登录后再试'
        return JsonResponse(data)

@is_login
def subcart(request):

    if request.method == 'POST':
        goods_id = request.POST.get('goods_id')
        user = request.user
        data = {}
        if user.id:
            data = {
                'code': 200,
                'msg': '请求成功'
            }
            user_cart = CartModel.objects.filter(user=user, goods_id=goods_id).first()

            if user_cart:
                if user_cart.c_num == 1:
                    user_cart.delete()
                    user_cart.c_num = 0
                else:
                    user_cart.c_num -= 1
                    user_cart.save()
                data['c_num'] = user_cart.c_num
                return JsonResponse(data)
        data['msg'] = '未登录,请登录后再试'
        return JsonResponse(data)


class Api_cartmodel(mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = CartModel.objects.all()
    serializer_class = SerializerCart

@is_login
def cart(request):
    if request.method == 'GET':
        user = request.user
        user_carts = CartModel.objects.filter(user=user.id)
        ctx = {
            'user_carts': user_carts
        }
        return render(request, 'cart/cart.html', ctx)


def change_cart_select(request):
    if request.method == 'GET':
        return redirect('axf:cart')
    if request.method == 'POST':
        cart_id = request.POST.get('cart_id')
        cart = CartModel.objects.filter(id=cart_id).first()
        if cart.is_select:
            cart.is_select = False
        else:
            cart.is_select = True
        cart.save()
        data = {
            'code': 200,
            'msg': '请求成功',
            'is_select': cart.is_select
        }
        return JsonResponse(data)

@is_login
def total(request):
    if request.method == 'GET':
        user = request.user
        user_cart = CartModel.objects.filter(user_id=user.id)
        total = 0
        for cart in user_cart:
            if cart.is_select:
                total += cart.goods.price * cart.c_num
        data = {
            'total': round(total, 2)
        }
        return JsonResponse(data)

@is_login
def all_select(request):
    if request.method == 'POST':
        user = request.user
        user_cart = CartModel.objects.filter(user_id=user.id)
        is_selected = request.POST.get('is_selected')
        flag = False
        if is_selected == '1':
            CartModel.objects.filter(user=user).update(is_select=True)
        else:
            flag = True
            CartModel.objects.filter(user=user).update(is_select=False)
        data = {
            'code': 200,
            'cart_id': [cart_id.id for cart_id in user_cart],
            'flag': flag
        }
        return JsonResponse(data)

@is_login
def order(request):
    if request.method == 'GET':
        user = request.user
        # 创建订单
        o_num = get_ticket()
        order = OrderModel.objects.create(user=user, o_num=o_num)
        # 选择勾选的商品进行下单
        user_carts = CartModel.objects.filter(user=user, is_select=True)
        for carts in user_carts:
            # 创建商品和订单之间的关系
            OrderGoodsModel.objects.create(goods=carts.goods,
                                           order=order,
                                           goods_num=carts.c_num)
        user_carts.delete()

        return render(request, 'order/order_info.html', {'order': order})


def alipy(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        user_order = OrderModel.objects.filter(id=order_id).first()
        user_order.o_status = 1
        user_order.save()
        data = {
            'code': 200,
            'msg': '付款成功'
        }
        return JsonResponse(data)

@is_login
def order_list(request):
    if request.method == 'GET':
        user = request.user
        orders = OrderModel.objects.filter(user=user, o_status=0)
        return render(request, 'order/order_list_wait_pay.html', {'orders': orders})

@is_login
def order_payed(request):
    if request.method == 'GET':
        user = request.user
        orders = OrderModel.objects.filter(user=user, o_status=1)
        return render(request, 'order/order_list_payed.html', {'orders': orders})


def wait_pay_to_payed(request):
    if request.method == 'GET':
        order_id = request.GET.get('order_id')
        order = OrderModel.objects.filter(id=order_id).first()

        return render(request, 'order/order_info.html', {'order': order})


def receipt(request):
    if request.method == 'POST':
        o_num = request.POST.get('o_num')
        OrderModel.objects.filter(o_num=o_num).first().delect()
        return JsonResponse({'code': 200, 'msg': '确认成功'})
