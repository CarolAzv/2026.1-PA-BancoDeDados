from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from .serializers import (
    UsuarioSerializer, ClienteSerializer, 
    VendedorSerializer, PerfilVendedorSerializer, 
    ProdutoSerializer, EnderecoSerializer, 
    FormaPagamentoSerializer, PedidoSerializer, 
    ItemPedidoSerializer, LoginSerializer
)
from .models import (
    Usuario, Cliente, Vendedor, PerfilVendedor, 
    Produto, Endereco, FormaPagamento, Pedido, 
    ItemPedido
)
from .permissions import IsVendedor


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

class UsuarioViewSet(viewsets.ViewSet):

    def get_permissions(self):
        if self.action in ('signup', 'login'):
            return [AllowAny()]
        return [IsAuthenticated()]

    def signup(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.save()
            refresh = RefreshToken.for_user(usuario) # gera o par
            return Response(
                {'refresh': str(refresh),
                'access': str(refresh.access_token),
                'usuario': serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def login(self, request):
        usuario = get_object_or_404(Usuario, username=request.data.get('username'))
        if not usuario.check_password(request.data.get('password')):
            return Response({'detail': 'Credenciais inválidas.'},
                        status=status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken.for_user(usuario)
        return Response({'refresh': str(refresh),
                         'access': str(refresh.access_token),
                         'usuario': UsuarioSerializer(usuario).data})

    def perfil(self, request):
        return Response({'usuario': request.user.username,
                         'tipo': request.user.tipo,
                         'mensagem': f'Autenticado via JWT como {request.user.get_tipo_display()}!'})


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]


class VendedorViewSet(viewsets.ModelViewSet):
    queryset = Vendedor.objects.all()
    serializer_class = VendedorSerializer
    permission_classes = [IsAuthenticated]


class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    
    
    def get_permissions(self):
        # Qualquer autenticado pode listar/ver; só vendedor escreve
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsVendedor()]


class PerfilVendedorViewSet(viewsets.ModelViewSet):
    queryset = PerfilVendedor.objects.select_related('vendedor').all()
    serializer_class = PerfilVendedorSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoSerializer
    def get_queryset(self):
        return (Pedido.objects
                .select_related('cliente')
                .prefetch_related('itens__produto')
                .all())

class ItemPedidoViewSet(viewsets.ModelViewSet):
    queryset = ItemPedido.objects.select_related('pedido', 'produto').all()
    serializer_class = ItemPedidoSerializer