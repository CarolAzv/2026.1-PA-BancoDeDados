from django.contrib import admin
from .models import Cliente, Vendedor, Produto, PerfilVendedor, Pedido, ItemPedido

admin.site.register(Cliente)
admin.site.register(Vendedor)
admin.site.register(Produto)
admin.site.register(PerfilVendedor)
admin.site.register(Pedido)
admin.site.register(ItemPedido)