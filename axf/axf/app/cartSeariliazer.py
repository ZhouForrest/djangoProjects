from rest_framework import serializers

from app.models import CartModel


class SerializerCart(serializers.ModelSerializer):

    class Meta:
        model = CartModel
        fields = ['c_num', 'goods_id']