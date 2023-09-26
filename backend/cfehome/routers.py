from rest_framework.routers import DefaultRouter

from products.viewsets import ProductGenericViewSet

router = DefaultRouter()
router.register('products', ProductGenericViewSet, basename='products') #/v2/products in urls.py
print(router.urls)
urlpatterns = router.urls


# from products.viewsets import ProductViewSet
# router = DefaultRouter()
# router.register('products', ProductViewSet, basename='products') #/v2/products in urls.py
# print(router.urls)
# urlpatterns = router.urls