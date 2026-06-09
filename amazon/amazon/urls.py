from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.permissions import AllowAny
from backend.views import ClienteViewSet, VendedorViewSet, ProdutoViewSet, PerfilVendedorViewSet, PedidoViewSet, ItemPedidoViewSet, UsuarioViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework_simplejwt.views import (
    TokenObtainPairView, # login: devolve access + refresh
    TokenRefreshView, # renova o access usando o refresh
)

schema_view = get_schema_view(
    openapi.Info(
        title="Amazon API",
        default_version='v1',
        description="Documentação da API do Amazon",
        terms_of_service="https://www.google.com",
        contact=openapi.Contact(email="[EMAIL_ADDRESS]"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[AllowAny],
)

router = routers.DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'vendedores', VendedorViewSet, basename='vendedor')
router.register(r'produtos', ProdutoViewSet, basename='produto')
router.register(r'perfil_vendedores', PerfilVendedorViewSet, basename='perfil_vendedor')
router.register(r'pedidos', PedidoViewSet, basename='pedido')
router.register(r'itens_pedido', ItemPedidoViewSet, basename='item_pedido')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('login_jwt/', TokenObtainPairView.as_view(), name='login_jwt'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('api/signup/', UsuarioViewSet.as_view({'post': 'signup'}), name='signup'),
    path('api/login/', UsuarioViewSet.as_view({'post': 'login'}), name='login'),
    path('api/perfil/', UsuarioViewSet.as_view({'get': 'perfil'}), name='perfil'),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
