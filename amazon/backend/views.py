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

from .serializers import UsuarioSerializer, ProdutoSerializer, EnderecoSerializer, FormaPagamentoSerializer, PedidoSerializer, ItemPedidoSerializer
from .models import Usuario, Produto, Endereco, FormaPagamento, Pedido, ItemPedido
from .permissions import IsVendedor


class ClienteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para o modelo Cliente.
    Fornece automaticamente os endpoints list, create, retrieve,
    update, partial_update e destroy.
    """
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    # Habilita filtros, busca textual e ordenação via query params
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['nome', 'email'] # ?nome=Maria
    search_fields = ['nome', 'email'] # ?search=Maria
    ordering_fields = ['nome', 'data_cadastro'] # ?ordering=-data_cadastro


lass ProdutoViewSet(viewsets.ModelViewSet):
 queryset = Produto.objects.all()
 serializer_class = ProdutoSerializer
 def get_permissions(self):
 # Qualquer autenticado pode listar/ver; só vendedor escreve
 if self.action in ['list', 'retrieve']:
 return [IsAuthenticated()]
 return [IsAuthenticated(), IsVendedor()]


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

