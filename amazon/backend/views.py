from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from .serializers import UsuarioSerializer, ProdutoSerializer, EnderecoSerializer, FormaPagamentoSerializer, PedidoSerializer, ItemPedidoSerializer, ClienteSerializer, VendedorSerializer, PerfilVendedorSerializer, 
from .models import Usuario, Produto, Endereco, FormaPagamento, Pedido, ItemPedido, Cliente, Vendedor, PerfilVendedor
from .permissions import IsVendedor


class UsuarioViewSet(viewsets.ViewSet):

    def get_permissions(self):
        if self.action in ('signup', 'login'):
            return [AllowAny()]
        return [IsAuthenticated()]

    def signup(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.save()
            token = Token.objects.create(user=usuario)
            return Response(
                {'token': token.key, 'usuario': serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def login(self, request):
        usuario = get_object_or_404(Usuario, username=request.data.get('username'))
        if not usuario.check_password(request.data.get('password')):
            return Response({'detail': 'Credenciais inválidas.'},
                        status=status.HTTP_400_BAD_REQUEST)
        token, _ = Token.objects.get_or_create(user=usuario)
        return Response({'token': token.key,
                         'usuario': UsuarioSerializer(usuario).data})

    def perfil(self, request):
        return Response({'usuario': request.user.username,
                         'tipo': request.user.tipo,
                         'mensagem': f'Bem-vindo, {request.user.username}! Este é o seu perfil. Tipo de usuário: {request.user.get_tipo_display()}.'})

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class VendedorViewSet(viewsets.ModelViewSet):
    queryset = Vendedor.objects.all()
    serializer_class = VendedorSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

    def get_permision(self):
        # Qualquer autenticado pode listar/ver; só vendedor escreve
        if self.action in ['list', 'retrive']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsVendedor()]

class PerfilVendedorViewSet(viewsets.ModelViewSet):
    queryset = PerfilVendedor.objects.select_related('vendedor').all()
    serializer_class = PerfilVendedorSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoSerializer

    def get_queryset(self):
        return (pedido.objects
                .select_related('cliente')
                .prefetch_related('itens__produto')
                .all())

class ItemPedidoViewSet(viewsets.ModelViewSet):
    queryset = ItemPedido.objects.select_related('pedido', 'produto').all()
    serializer_class = ItemPedidoSerializer


@api_view(['POST'])
@permission_classes({AllowAny}) # registro é público
def signup(request):
    serializer = UsuarioSerializer(data=request.data)

    if serializer.is_valid():
        usuario = serializer.save() # chama o create() do serializer
        token = Token.objects.create(user=usuario)
        return Response({'token': token.key, 'usuario': serializer.data}, status=stauts.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes({AllowAny}) # login é público
def login(request):
    usuario = get_object_or_404(Usuario, username=request.data.get('username'))

    if not usuario.check_password(request.data.get('password')):
        return Response({'detail': 'Credenciais inválidas.'}, status=status.HTTP_400_BAD_REQUEST)

    token, _ = Token.objects.get_or_create(user=usuario)
    return Response({'token': token.key, 'usuario': UsuarioSerializer(usuario).data})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated]) # exige token válido
def perfil(request):
    return Response({
        'username': request.user.username,
        'tipo': request.user.tipo,
        'mensagem': f'Olá, {request.user.username}! 
        Você é {request.user.get_tipo_display()}.'
    })

