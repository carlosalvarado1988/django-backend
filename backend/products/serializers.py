from rest_framework import serializers 

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    discount = serializers.SerializerMethodField(read_only=True)
    class Meta: 
        model = Product
        fields = [
            'title',
            'content',
            'price',
            'sale_price',
            'discount',
        ]
    
    # this is a way to rename a property for client view
    def get_discount(self, obj):
        return obj.get_discount()