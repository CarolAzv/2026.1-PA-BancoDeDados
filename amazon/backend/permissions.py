from rest_framework.permissions import BasePermission

class IsVendedor(BasePermission):
    message = 'Apenas vendedores podem realizar esta ação.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated
            and request.user.is_vendedor())
