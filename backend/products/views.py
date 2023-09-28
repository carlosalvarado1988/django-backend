from rest_framework import generics, mixins #authentication, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from api.mixins import (UserQuerySetMixin, StaffEditorPermissionMixin)
from api.authentication import TokenAuthentication
from .models import Product
# from ..api.permissions import IsStaffEditorPermission
from .serializers import ProductSerializer


# THESE ARE KNOW AS CLASS BASED VIEW
class ProductListCreateAPIView(
    UserQuerySetMixin, 
    StaffEditorPermissionMixin, 
    generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    print('We are in ProductListCreateAPIView')
    # Authentication module
    # authentication_classes = [
    #     authentication.SessionAuthentication,
    #     authentication.TokenAuthentication // using  built in keywork 'Token'
    # ]

    # After adding the default in settings.py using the docuemntaiton, we dont need to declare it in the view of the product itself.
    # authentication_classes = [
    #     authentication.SessionAuthentication,
    #     TokenAuthentication # using custom module with keywork 'Bearer'
    # ]

    # implementing the permission (middleware) from rest_framework
    # apparently just by creating the permission_classes definition, the framework recongnizes it and it starts working

    # this one prevents any method if not authenticated
    # permission_classes = [permissions.IsAuthenticated]
    
    # this one allows list but not create
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # This one is from DjangoModel, meaning it bases permission based on the user itself, 
    # according to what was setup in the admin pannel or via the CLI user creation
    # permission_classes = [IsStaffEditorPermission]

    # Lastly, we can manage permissions in the way of an array.    
    # even having the default GET permisson in the default settings.py, we want to keep these custom ones
    # permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission] #commented since we implemented the mixin at the top level

    def perform_create(self, serializer):
        # this could be one line method to save a user in the serializer
        # serializer.save(user=self.request.user)
        print('WE ARE HERE IN ProductListCreateAPIView')
        print(serializer.validated_data)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title
        serializer.save(user=self.request.user, content=content)

    # since we added the user to the serializer, to be part of the product object, we want to add that during creation.
    # def get_queryset(self, *args, **kwargs):
    #     qs=super().get_queryset(*args, **kwargs)
    #     user=self.request.user
    #     # print(user)
    #     if not user.is_authenticated:
    #         return Product.objects.none()
    #     return qs.filter(user=user)
    # we commented this because it was moved to the mixins.py and imported as a dependency injection
        

product_list_create_view = ProductListCreateAPIView.as_view()

class ProductDetailsAPIView(UserQuerySetMixin, StaffEditorPermissionMixin, generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = 'pk'
product_detail_view = ProductDetailsAPIView.as_view()

class ProductUpdateAPIView(UserQuerySetMixin, StaffEditorPermissionMixin, generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    ## all of this is a method inside to perform the db update
    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title

product_update_view = ProductUpdateAPIView.as_view()


class ProductDestroyAPIView(UserQuerySetMixin, StaffEditorPermissionMixin, generics.DestroyAPIView):
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


class ProductMixinView(UserQuerySetMixin, StaffEditorPermissionMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
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