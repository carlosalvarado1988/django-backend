from rest_framework import generics, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Product
from .serializers import ProductSerializer


# THESE ARE KNOW AS CLASS BASED VIEW
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        # this could be one line method to save a user in the serializer
        # serializer.save(user=self.request.user)
        print(serializer.validated_data)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title
        serializer.save(content=content)

product_list_create_view = ProductListCreateAPIView.as_view()

class ProductDetailsAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = 'pk'
product_detail_view = ProductDetailsAPIView.as_view()

class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    ## all of this is a method inside to perform the db update
    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title

product_update_view = ProductUpdateAPIView.as_view()


class ProductDestroyAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        # instance
        super().perform_destroy(instance)

product_destroy_view = ProductDestroyAPIView.as_view()

# **
# Not needed because we are using ProductListCreateAPIView
# **
# class ProductLisAPIView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


class ProductMixinView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    #HTTP --> GET
    def get(self, request, *args, **kwargs): 
        # self here refers to all the methods existing in the parameters added in the class as injection, 
                # list method is within ListModelMixin, retrieve is within RetrieveModelMixin.

        # here we grab pk from the args passed in the url. (like /? args)
        print("args and kwargs:")
        print(args, kwargs)
        pk = kwargs.get('pk')

        # checking if there is a pk, then we do retrieve to get one single data from db
        if pk is not None:
            # retrieve is within RetrieveModelMixin.
            return self.retrieve(request, *args, **kwargs)
        # otherwise, we do a list
        # list method is within ListModelMixin 
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        # create method is within CreateModelMixin 
        return self.create(request, *args, **kwargs)

    # this could be one line method to save a user in the serializer
    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = 'As a test, Im adding data if empty to my content field. created view single view with mixings create'
        serializer.save(content=content)
        # sends a Django signal


product_mixin_view = ProductMixinView.as_view()



# This is a custom way to create a view that does the same of the above generics.
# we could add also update and delete methods to be handled in this one alterantive
# THESE ARE KNOW AS FUNCTION BASED VIEW
# ALL CRUD
@api_view(['GET', 'POST'])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method
    
    if method == "GET":
        if pk is not None:
            # get request -> detail view
            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(obj,  many=False).data
            return Response(data)
        # list view 
        queryset = Product.objects.all()
        data = ProductSerializer(queryset, many=True).data
        return Response(data)

    if method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content') or None
            if content is None:
                content = title 
            serializer.save(content=content)
            return Response(serializer.data)
        return Response({"Invalid":"not good data"}, status= 400)