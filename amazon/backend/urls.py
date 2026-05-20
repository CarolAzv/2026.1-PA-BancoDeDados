# backend/urls.pyfrom django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('produtos', views.ProdutoViewSet, basename='produto')

urlpatterns = [
    path('signup/', views.signup),
    path('login/', views.login),
    path('perfil/', views.perfil),
    path('', include(router.urls)),
]