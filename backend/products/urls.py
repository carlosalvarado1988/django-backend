from django.urls import path

from . import views

urlpatterns = [
    # path('', views.ProductListCreateAPIView.as_view()),
    # path('<int:pk>/', views.ProductDetailsAPIView.as_view())
    path('', views.product_alt_view),
    path('<int:pk>/', views.product_alt_view),
]