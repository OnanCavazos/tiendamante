from django.contrib import admin
from .models import Producto, Usuario, Pedido, DetallePedido, Mensaje

# -----------------------------
# Producto
# -----------------------------
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'precio', 'categoria')
    search_fields = ('nombre', 'categoria')
    list_filter = ('categoria',)
    list_per_page = 25


# -----------------------------
# Usuario
# -----------------------------
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'correo', 'fecha_registro')
    search_fields = ('nombre', 'correo')
    list_filter = ('fecha_registro',)
    readonly_fields = ('fecha_registro',)


# -----------------------------
# Pedido
# -----------------------------
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fecha', 'total')
    search_fields = ('id', 'usuario__username')
    list_filter = ('fecha',)
    readonly_fields = ('fecha',)


# -----------------------------
# DetallePedido
# -----------------------------
@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'pedido', 'producto', 'cantidad', 'precio')
    search_fields = ('pedido__id', 'producto__nombre')
    list_filter = ('pedido',)


# -----------------------------
# Mensaje
# -----------------------------
@admin.register(Mensaje)
class MensajeAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'correo', 'fecha')
    search_fields = ('nombre', 'correo', 'mensaje')
    list_filter = ('fecha',)
    readonly_fields = ('fecha',)





