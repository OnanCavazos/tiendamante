from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from Principal.models import Producto
from Principal.forms import MensajeForm
from Principal.models import Pedido, DetallePedido

# =============================
# 🏠 Página principal
# =============================
def index(request):
    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tu mensaje fue enviado correctamente.")
            return redirect('index')
    else:
        form = MensajeForm()
    return render(request, 'index.html', {'form': form})

# =============================
# 📦 Catálogo
# =============================
def catalogo(request):
    productos = Producto.objects.all()
    return render(request, 'catalogo.html', {'productos': productos, 'titulo': 'Catálogo completo'})

def catalogo_electronica(request):
    productos = Producto.objects.filter(categoria='electronica')
    return render(request, 'catalogo_categoria.html', {'productos': productos, 'titulo': 'Electrónica'})

def catalogo_ropa(request):
    productos = Producto.objects.filter(categoria='ropa')
    return render(request, 'catalogo_categoria.html', {'productos': productos, 'titulo': 'Ropa'})

def catalogo_electrodomesticos(request):
    productos = Producto.objects.filter(categoria='electrodomesticos')
    return render(request, 'catalogo_categoria.html', {'productos': productos, 'titulo': 'Electrodomésticos'})

def catalogo_accesorios(request):
    productos = Producto.objects.filter(categoria='accesorios')
    return render(request, 'catalogo_categoria.html', {'productos': productos, 'titulo': 'Accesorios'})

# =============================
# 📄 Páginas secundarias
# =============================
def acerca(request):
    return render(request, 'acercade.html')

def contacto(request):
    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tu mensaje fue enviado correctamente.")
            return redirect('contacto')
    else:
        form = MensajeForm()
    return render(request, 'contacto.html', {'form': form})

def guardar_contacto(request):
    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Mensaje guardado correctamente.")
            return redirect('index')
        else:
            messages.error(request, "Error al enviar el mensaje.")
            return redirect('contacto')
    else:
        return redirect('contacto')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cuenta creada correctamente.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# =============================
# 🛒 Carrito — utilidades
# =============================
def _obtener_carrito(request):
    """Obtiene el carrito actual desde la sesión."""
    return request.session.get('carrito', {})

def _guardar_carrito(request, carrito):
    """Guarda el carrito actualizado en la sesión."""
    request.session['carrito'] = carrito
    request.session.modified = True

# =============================
# 🛒 Carrito — acciones
# =============================
from django.views.decorators.http import require_POST

@require_POST
def agregar_al_carrito(request, producto_id):
    """Agrega un producto al carrito."""
    producto = get_object_or_404(Producto, id=producto_id)
    cantidad = int(request.POST.get('cantidad', 1))
    if cantidad < 1:
        cantidad = 1

    carrito = _obtener_carrito(request)
    key = str(producto_id)

    if key in carrito:
        carrito[key]['cantidad'] += cantidad
    else:
        carrito[key] = {
            'nombre': producto.nombre,
            'precio': float(producto.precio),
            'cantidad': cantidad,
        }

    _guardar_carrito(request, carrito)
    messages.success(request, f"Se agregó {cantidad} unidad(es) de '{producto.nombre}' al carrito.")
    return redirect('carrito')

def carrito(request):
    """Muestra el carrito con productos y total."""
    raw = _obtener_carrito(request)

    # Preparamos items con id y subtotal ya calculado para no hacer aritmética en template
    items = []
    total = 0.0
    for pid, item in raw.items():
        subtotal = float(item['precio']) * int(item['cantidad'])
        total += subtotal
        items.append({
            'id': int(pid),
            'nombre': item['nombre'],
            'precio': float(item['precio']),
            'cantidad': int(item['cantidad']),
            'subtotal': subtotal,
        })

    contexto = {
        'items': items,
        'total': total,
    }
    return render(request, 'carrito.html', contexto)

@require_POST
def actualizar_carrito(request, producto_id):
    """Modifica la cantidad de un producto."""
    carrito = _obtener_carrito(request)
    key = str(producto_id)
    if key in carrito:
        cantidad = int(request.POST.get('cantidad', 1))
        if cantidad > 0:
            carrito[key]['cantidad'] = cantidad
            messages.success(request, "Cantidad actualizada.")
        else:
            del carrito[key]
            messages.info(request, "Producto eliminado del carrito.")
        _guardar_carrito(request, carrito)
    return redirect('carrito')

def eliminar_del_carrito(request, producto_id):
    """Elimina un producto del carrito."""
    carrito = _obtener_carrito(request)
    key = str(producto_id)
    if key in carrito:
        del carrito[key]
        _guardar_carrito(request, carrito)
        messages.info(request, "Producto eliminado del carrito.")
    return redirect('carrito')

# =============================
# 💳 Procesar pago
# =============================
@require_POST
def procesar_pago(request):
    """Simula el pago: valida carrito, calcula total, vacía y muestra confirmación."""
    raw = _obtener_carrito(request)
    if not raw:
        messages.error(request, "Tu carrito está vacío, no puedes procesar el pago.")
        return redirect('carrito')

    total = sum(float(i['precio']) * int(i['cantidad']) for i in raw.values())

    # Vaciar el carrito
    request.session['carrito'] = {}
    request.session.modified = True

    # Render directo con total pagado
    return render(request, 'procesar_pago.html', {'total': total})

def procesar_pago(request):
    carrito = request.session.get("carrito", {})

    if not carrito:
        messages.error(request, "Tu carrito está vacío.")
        return redirect("carrito")

    total = sum(item["precio"] * item["cantidad"] for item in carrito.values())

    # ✅ Crear pedido
    pedido = Pedido.objects.create(
        usuario=request.user if request.user.is_authenticated else None,
        total=total
    )

    # ✅ Guardar detalles del pedido
    for product_id, item in carrito.items():
        DetallePedido.objects.create(
            pedido=pedido,
            producto=Producto.objects.get(id=product_id),
            cantidad=item["cantidad"],
            precio=item["precio"]
        )

    # ✅ Vaciar carrito
    request.session["carrito"] = {}
    request.session.modified = True

    messages.success(request, "✅ ¡Compra realizada correctamente!")
    return render(request, "procesar_pago.html", {"pedido": pedido})


# =============================
# ✅ HISTORIAL DE PEDIDOS
# =============================
def mis_pedidos(request):
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para ver tus pedidos.")
        return redirect("login")

    pedidos = Pedido.objects.filter(usuario=request.user).order_by("-fecha")
    return render(request, "mis_pedidos.html", {"pedidos": pedidos})


def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if pedido.usuario != request.user:
        messages.error(request, "No tienes permiso para ver este pedido.")
        return redirect("mis_pedidos")

    return render(request, "detalle_pedido.html", {"pedido": pedido})