"""
URL configuration for ecommerce_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from productApp.views import ProductViewSet, indexView, productListView, categoryListView, categoryDetailView, ProductAPIView, ProductListCreateView, ProductGenericAPIView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'products-viewset', ProductViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", indexView),
    path('product-list/', productListView),
    path('category/', categoryListView),
    path('category/<int:id>/', categoryDetailView),
    path('product-apiview/', ProductAPIView.as_view()),
    path('product-apiview/<int:id>/', ProductAPIView.as_view()),
    path('product-list-create/', ProductListCreateView.as_view()),
    path('product-generic-apiview/<int:id>/', ProductGenericAPIView.as_view()),
    path('product-generic-apiview/', ProductGenericAPIView.as_view()),
    path('accounts/', include('accounts.urls')),
    path('', include(router.urls)),
]
 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)