import json
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.response import Response

from products.serializers import ProductSerializer
from products.models import Product
from django.http import JsonResponse, HttpResponse

@api_view(["POST"])
def api_home(request, *args, **kwargs):
    print(request.data)
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        # instance = serializer.save()
        print(serializer.data)
        return Response(serializer.data)
    return Response({"Invalid":"not good data"}, status= 400)

    # @api_view(["GET"])
    # instance = Product.objects.all().order_by("?").first()
    # data = {}
    # if instance:
    #     data = ProductSerializer(instance).data
    # return Response(data)