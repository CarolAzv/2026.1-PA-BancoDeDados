from .models import Cliente, Endereco, FormaPagamento, Vendedor, Item, Pedido, ItemPedido
from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'password', 'tipo', 'cpf', 'telefone']

    def create(self, validated_data):
        # create_user faz o hash da senha corretamente
        senha = validated_data.pop('password')
        usuario = Usuario(**validated_data)
        usuario.set_password(senha)
        usuario.save()
        return usuario

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = '__all__'

class FormaPagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormaPagamento
        fields = '__all__'

class VendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendedor
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'

class ItemPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPedido
        fields = '__all__'

class PerfilVendedorSerializer(serializers.ModelSerializer):
    vendedor_id = serializers.IntegerField(source='vendedor.id')    
    vendedor_nome = serializers.CharField(source='vendedor.nome', read_only=True) 
    
    def validate(self, attrs):
        vendedor_data = attrs.get('vendedor', {})
        vendedor_id = vendedor_data.get('id') if isinstance(vendedor_data, dict) else None
        if vendedor_id is None:
            raise serializers.ValidationError({'vendedor_id': 'Este campo é obrigatório.'})
        try:
            attrs['vendedor'] = Vendedor.objects.get(id=vendedor_id)
        except Vendedor.DoesNotExist:
            raise serializers.ValidationError({'vendedor_id': f'Vendedor com id={vendedor_id} não encontrado.'})
        return attrs

    class Meta:
        model = PerfilVendedor
        fields = ['vendedor_id', 'vendedor_nome', 'razao_social','inscricao_estadual', 'banco', 'agencia','conta', 'chave_pix']
    