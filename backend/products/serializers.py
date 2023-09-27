from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Product
from . import validators
from api.serializers import UserPublicSerializer

class ProductSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(source='user', read_only=True) #Django maps automaticall to the user, if we change the key, we need to declare the source
    discount = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    # this HyperlinkedIdentityField is a shortcut method to build a hyperlink, it only works with ModelSerializer
    url = serializers.HyperlinkedIdentityField(
         view_name='product-detail',
         lookup_field='pk'
    )
    # we added this line so that we implement validation from the imported file
    title=serializers.CharField(validators=[validators.unique_product_title, validators.validate_title_no_test])
    # email = serializers.EmailField(write_only=True)
    # this is an example on how to grab a value to be added to another , title to name
    # name=serializers.CharField(source='title', read_only=True)

    class Meta: 
        model = Product
        fields = [
            'owner', #we can comment this after we ensure, we save user data on create in the view
            'url',
            'edit_url',
            'pk',
            # 'email',
            'title',
            # 'name',
            'content',
            'price',
            'sale_price',
            'discount',
        ]
    
    # this is a way to autocomplete the url value for the field, how does "url" listed in the fields array fetches whats in the get_url def function?
    # apparently this is part of the magic of django, connecting the field with its get_ prefix, the same happens with disccount.
    # def get_url(self, obj):
    #     return f'/api/products/{obj.id}'
    
    # another elegant way is to use the built-in reverse() function from rest_framework
    # as the first argument of the reverse func, we need to reference the name of the url, so we added this extra param to the urls.py in products dir.
    # def get_url(self, obj):
    #     request = self.context.get('request') #self.request
    #     if request is None:
    #         return None
    #     return reverse('product-detail', kwargs={'pk': obj.id}, request=request)
    
    # note that we can also use the
    def get_edit_url(self, obj):
        request = self.context.get('request') #self.request
        if request is None:
            return None
        return reverse('product-edit', kwargs={'pk': obj.id}, request=request)

    # this is a way to rename a property for client view
    def get_discount(self, obj):
            if not hasattr(obj, "id"):
                return None
                
            if not isinstance(obj, Product):
                return None
            return obj.get_discount()
        # try:
        # except:
        #     return None

    # def create(self, validated_data):
    #     # return Product.objects.create(**validated_data)
    #     email= validated_data.pop('email')
    #     obj = super().create(validated_data)
    #     print(email, obj)
    #     return obj

    # VALIDATION EXAPLES - after testing we moved it to validators.py
    # def validate_title(self, value):
    #     #  query to check if value exists in db = iexact means case insensitive
    #      qs = Product.objects.filter(title__iexact=value)
    #      if qs.exists():
    #           raise serializers.ValidationError(f"{value} already exists as a product name")
    #      return value