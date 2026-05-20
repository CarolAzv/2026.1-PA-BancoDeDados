from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    class Tipo(models.TextChoices):
        CLIENTE = 'CLIENTE', 'Cliente'
        VENDEDOR = 'VENDEDOR', 'Vendedor'

    tipo = models.CharField(
        max_length=10,
        choices=Tipo.choices,
        default=Tipo.CLIENTE,
    )

    cpf = models.CharField(max_length=11, unique=True)
    telefone = models.CharField(max_length=15, blank=True)

    def is_cliente(self):
        return self.tipo == self.Tipo.CLIENTE
    def is_vendedor(self):
        return self.tipo == self.Tipo.VENDEDOR
    def __str__(self):
        return f'{self.username} ({self.get_tipo_display()})'


class Cliente(models.Model):
    nome = models.CharField(max_length=255, null=False, blank=False) # NOT NULL no banco
    email = models.EmailField(unique=True) # UNIQUE no banco
    telefone = models.CharField(max_length=15, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True) # Preenchido automaticamente

    #class Meta:
    #    db_table = 'clientes' # Nome explícito da tabela no banco
    #    ordering = ['nome'] # Ordenação padrão nas consultas

    def __str__(self):
        return f"{self.nome} - {self.email} - {self.telefone or 'Sem telefone'}"


class Endereco(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='enderecos')
    rua = models.CharField(max_length=255)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    cep = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.rua}, {self.cidade} - {self.estado} ({self.cep})"


class FormaPagamento(models.Model):
    tipo = models.CharField(max_length=50)

    def __str__(self):
        return self.tipo


class Vendedor(models.Model):
    nome = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(unique=True, default='email@exemplo.com')
    cpf_cnpj = models.CharField(max_length=14, unique=True, default='')
    telefone = models.CharField(max_length=15)
    avaliacao = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nome} - {self.email} - {self.telefone}'

class Produto(models.Model):
    vendedor = models.ForeignKey(
        Vendedor,
        on_delete=models.PROTECT, #nao pode deletar um vendedor que tem produtos
        related_name='produtos',
        null=True,
        blank=True
    ) 
    nome = models.CharField(max_length=255, null=False, blank=False)
    preco = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    descricao = models.TextField()
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nome} - {self.preco} - {self.data_cadastro}'

class PerfilVendedor(models.Model):
    vendedor = models.OneToOneField(
        Vendedor,
        on_delete=models.CASCADE,
        related_name='perfil',
        primary_key=True
    )

    razao_social = models.CharField(max_length=150, blank=True)
    inscricao_estadual = models.CharField(max_length=20, blank=True)
    banco = models.CharField(max_length=50, blank=True)
    agencia = models.CharField(max_length=10, blank=True)
    conta = models.CharField(max_length=20, blank=True)
    chave_pix = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'Perfil de {self.vendedor.nome}'

class Pedido(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('enviado', 'Enviado'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    ]
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name='pedidos'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente'
    )
    data_pedido = models.DateTimeField(auto_now_add=True)
    observacoes = models.TextField(blank=True)

    def __str__(self):
        return f'Pedido #{self.id} de {self.cliente.nome} - Status: {self.status}'

class ItemPedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE, #pode deletar um pedido mesmo que ele tenha itens
        related_name='itens'
    )
    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT, #nao pode deletar um produto que esta em um pedido
        related_name='itens_pedido'
    )
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, editable=False) # o preco unitario nao pode ser alterado


    def __str__(self):
        return f'{self.quantidade} x {self.produto.nome} em #{self.pedido.id}'

    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario