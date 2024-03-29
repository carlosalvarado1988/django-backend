"""cfehome URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from products import views
from cfehome.views import index

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')), # host:800/api/
    path('api/search/', include('search.urls')), # host:800/api/search/
    path('api/products/', include('products.urls')), # host:800/api/products/
    path('api/v2/', include('cfehome.routers')), # our v2 routers version

]

