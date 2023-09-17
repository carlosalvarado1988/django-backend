from django.urls import path

from . import views

urlpatterns = [
    # path('', views.product_list_create_view), #dedicated view - client/list.py
    # path('<int:pk>/', views.product_detail_view), #dedicated view - client/detail.py
    path('<int:pk>/update/', views.product_update_view), #dedicated view
    path('<int:pk>/delete/', views.product_destroy_view), #dedicated view
    path('', views.product_mixin_view), #using one mixing view - client/list.py
    path('<int:pk>/', views.product_mixin_view), #using one mixing view - client/detail.py
    # path('', views.product_alt_view),
    # path('<int:pk>/', views.product_alt_view),
] 