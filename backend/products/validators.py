
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Product

# def validate_title(value):
#     #  query to check if value exists in db = iexact means case insensitive
#         qs = Product.objects.filter(title__iexact=value)
#         if qs.exists():
#             raise serializers.ValidationError(f"{value} already exists as a product name")
#         return value


# another way to do some built-in validation or enhanced
unique_product_title = UniqueValidator(queryset=Product.objects.all(), lookup='iexact')

def validate_title_no_test(value):
    if "test" in value.lower():
        raise serializers.ValidationError(f"Test word is not allowed")
    
    return value
