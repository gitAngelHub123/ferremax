from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Post, SolicitudArticulo, CartItem
from .forms import *
from FerreMaX import settings
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Post, CartItem
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Post, CartItem
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Post
import paypalrestsdk
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import CartItem, Order, OrderItem
import datetime
import random
import string
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Order
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from .models import Post  # Asegúrate de que el modelo está importado correctamente
from django.shortcuts import render, redirect
from .models import Order
from django.db.models import Q  
from django.shortcuts import render, get_object_or_404
from .models import Order
from django.shortcuts import render
from django.db.models import Sum
from .models import OrderItem
import io
import matplotlib.pyplot as plt # type: ignore
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from .models import OrderItem
from django.db.models import Sum
from datetime import datetime
import uuid
from django.shortcuts import render, redirect
from .models import Proveedor
from .forms import ProveedorForm
from .decorators import user_has_role, redirect_authenticated_user
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.conf import settings
from .models import Post, Order, OrderItem, CartItem
import paypalrestsdk
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CustomPasswordChangeForm
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .forms import RecuperarContrasenaForm
from .models import User,Fallo
from django.http import HttpResponseRedirect
# Vistas de autenticación y registro


def base(request):
    zero_stock_products = Post.objects.filter(stock=0).exists()
    return {'zero_stock_products': zero_stock_products}




def buscar(request):
    query = request.GET.get('q')
    if query:
        # Lógica para buscar la URL según la query
        if query == "home":
            return redirect('home')
        elif query == "base":
            return redirect('base')
        elif query == "Productos":
            return redirect('product_list')
        elif query == "registro":
            return redirect('registro')
        elif query == "iniciar sesion":
            return redirect('inicio_sesion')
        else:
            # En caso de que no encuentre ninguna coincidencia, puedes redirigir a una página de error o simplemente a la página principal.
            return redirect('home')
    else:
        # En caso de que no se proporcione ninguna query, redirigir a la página principal.
        return redirect('home')




def registro_cliente(request):
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.tipo_de_cuenta = 'cliente'
            usuario.save()
            messages.success(request, 'Usuario registrado exitosamente.')
            return redirect('home')
    else:
        form = RegistroClienteForm()
    return render(request, 'app/registroUsuario.html', {'form': form})




@user_has_role('administrador')
def registro_administrador(request):
    if request.method == 'POST':
        form = RegistroAdministradorForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.tipo_de_cuenta = 'administrador'
            usuario.save()
            messages.success(request, 'Usuario registrado exitosamente.')
            return redirect('home')
    else:
        form = RegistroAdministradorForm()
    return render(request, 'app/registro_administrador.html', {'form': form})




@user_has_role('administrador')
def registro_trabajador(request):
    if request.method == 'POST':
        form = RegistroTrabajadorForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.tipo_de_cuenta = 'trabajador'
            usuario.save()
            messages.success(request, 'Usuario registrado exitosamente.')
            return redirect('home')
    else:
        form = RegistroTrabajadorForm()
    return render(request, 'app/registro_trabajador.html', {'form': form})


@login_required
def perfil_usuario(request):
    usuario = request.user
    return render(request, 'app/perfil_usuario.html', {'usuario': usuario})

@login_required
def editar_usuario(request):
    if request.method == 'POST':
        form = EditarUsuarioForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado.')
            return redirect('editar_usuario')
    else:
        form = EditarUsuarioForm(instance=request.user)
    
    return render(request, 'app/editar_usuario.html', {'form': form})



@login_required
def cambiar_contrasena(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Esto es importante para que el usuario no se desconecte después de cambiar la contraseña
            messages.success(request, 'Tu contraseña ha sido cambiada exitosamente.')
            return redirect('perfil_usuario')
        else:
            messages.error(request, 'Por favor corrige los errores a continuación.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'app/cambiar_contrasena.html', {'form': form})


@redirect_authenticated_user
def inicio_sesion(request):
    if request.method == 'POST':
        form = InicioSesionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenido {user.username}!')
                if user.tipo_de_cuenta == 'cliente':
                    return redirect('home')
                else:
                    return redirect('home')
    else:
        form = InicioSesionForm()
    return render(request, 'app/inicio_sesion.html', {'form': form})





def recuperar_contrasena(request):
    if request.method == 'POST':
        form = RecuperarContrasenaForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            nombre = form.cleaned_data['nombre']
            apellidos = form.cleaned_data['apellidos']
            try:
                user = User.objects.get(username=username, nombre=nombre, apellidos=apellidos)
                messages.success(request, f'Tu contraseña es: {user.password}')
            except User.DoesNotExist:
                messages.error(request, 'No se encontró un usuario con la información proporcionada.')
    else:
        form = RecuperarContrasenaForm()
    return render(request, 'app/recuperar_contrasena.html', {'form': form})

def cerrar_sesion(request):
    logout(request)
    return redirect('home')




@user_has_role('cliente', 'trabajador', 'administrador')
def solicitud_articulo(request):
    if request.method == 'POST':
        form = SolicitudArticuloForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('solicitud_exitosa')  # Asegúrate de tener una URL con este nombre
    else:
        form = SolicitudArticuloForm()
    return render(request, 'app/solicitarArticulo.html', {'form': form})

def solicitud_exitosa(request):
    return render(request, 'app/solicitud_exitosa.html')


@user_has_role('trabajador', 'administrador')
def listar_solicitudes(request):
    solicitudes = SolicitudArticulo.objects.all()
    return render(request, 'app/listar_solicitudes.html', {'solicitudes': solicitudes})



def eliminar_solicitud(request, numero_solicitud):
    solicitud = get_object_or_404(SolicitudArticulo, numeroSolicitud=numero_solicitud)
    solicitud.delete()
    return redirect('listar_solicitudes')



def home(request):
    categoria = request.GET.get('categoria')
    query = request.GET.get('query')
    orden = request.GET.get('orden')
    
    productos = Post.objects.all()
    
    if categoria:
        productos = productos.filter(categoria=categoria)
    
    if query:
        productos = productos.filter(Producto__icontains=query)
    
    if orden == 'asc':
        productos = productos.order_by('precio')
    elif orden == 'desc':
        productos = productos.order_by('-precio')
    
    categorias = Post.objects.values_list('categoria', flat=True).distinct()
    
    return render(request, 'app/home.html', {
        'productos': productos,
        'categorias': categorias,
        'categoria_seleccionada': categoria,
        'query': query,
        'orden': orden
    })

#carrito 




def add_to_cart(request, product_id):
    product = get_object_or_404(Post, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    if product.stock <= 0:
        messages.error(request, 'Producto agotado')
        return redirect('product_list')

    cart_item, created = CartItem.objects.get_or_create(product=product)
    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity
    cart_item.save()

    return redirect('cart_detail')

@user_has_role('cliente', 'trabajador', 'administrador')
def cart_detail(request):
    cart_items = CartItem.objects.all()
    total_price = sum(item.get_total_price() for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'app/cart_detail.html', context)

def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart_detail')

@user_has_role('cliente', 'trabajador', 'administrador')
def product_list(request):
    name = request.GET.get('name', '')
    category = request.GET.get('category', '')
    price_order = request.GET.get('price_order', '')

    products = Post.objects.all()

    if name:
        products = products.filter(Producto__icontains=name)
    
    if category:
        products = products.filter(categoria__icontains=category)
    
    if price_order:
        if price_order == 'asc':
            products = products.order_by('precio')
        elif price_order == 'desc':
            products = products.order_by('-precio')
    
    paginator = Paginator(products, 12)  # Muestra 12 productos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Post.objects.values_list('categoria', flat=True).distinct()

    return render(request, 'app/Productos.html', {
        'page_obj': page_obj,
        'categories': categories,
        'name': name,
        'category': category,
        'price_order': price_order,
    })

#paypal




def generate_order_number():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


@user_has_role('cliente', 'trabajador', 'administrador')
@login_required
def process_payment(request):
    # Configurar PayPal SDK
    paypalrestsdk.configure({
        'mode': 'sandbox',  # Cambiar a 'live' en producción
        'client_id': settings.PAYPAL_CLIENT_ID,
        'client_secret': settings.PAYPAL_CLIENT_SECRET,
    })

    # Obtener los ítems del carrito
    cart_items = CartItem.objects.all()
    total_price_clp = sum(item.get_total_price() for item in cart_items)

    # Obtener la tasa de cambio de CLP a USD
    response = requests.get('https://mindicador.cl/api')
    if response.status_code != 200:
        messages.error(request, "No se pudo obtener la tasa de cambio. Inténtelo de nuevo más tarde.")
        return redirect('order_list')
    
    exchange_rates = response.json()
    clp_to_usd_rate = exchange_rates.get('dolar', {}).get('valor', None)
    if clp_to_usd_rate is None:
        messages.error(request, "No se pudo obtener la tasa de cambio. Inténtelo de nuevo más tarde.")
        return redirect('order_list')

    # Convertir el precio total a USD
    total_price_usd = total_price_clp / clp_to_usd_rate

    # Crear el pago en PayPal
    payment = paypalrestsdk.Payment({
        'intent': 'sale',
        'payer': {
            'payment_method': 'paypal'
        },
        'redirect_urls': {
            'return_url': request.build_absolute_uri(reverse('payment_done')),
            'cancel_url': request.build_absolute_uri(reverse('payment_failed')),
        },
        'transactions': [{
            'item_list': {
                'items': [{
                    'name': item.product.Producto,
                    'sku': item.product.id,
                    'price': str(round(item.product.precio / clp_to_usd_rate, 2)),
                    'currency': 'USD',  # Cambiar a USD
                    'quantity': item.quantity,
                } for item in cart_items]
            },
            'amount': {
                'total': str(round(total_price_usd, 2)),
                'currency': 'USD'  # Cambiar a USD
            },
            'description': 'Compra en FerreMaX'
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == 'approval_url':
                request.session['order_data'] = {
                    'total_price': total_price_usd,
                    'items': [{'product': item.product.id, 'quantity': item.quantity, 'price': item.product.precio} for item in cart_items]
                }
                return redirect(link.href)
    else:
        messages.error(request, f"Error en el pago: {payment.error['message']}")
        return render(request, 'error.html', {'error': payment.error})
def payment_done(request):
    order_data = request.session.get('order_data')
    if not order_data:
        return redirect('product_list')
    
    order = Order.objects.create(
        user=request.user,
        order_number=generate_order_number(),
        total_price=order_data['total_price'],
        direccion=request.user.direccion  # Almacenar la dirección del usuario
    )

    for item_data in order_data['items']:
        product = get_object_or_404(Post, id=item_data['product'])
        quantity = item_data['quantity']
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=item_data['price']
        )
        # Reducir el stock del producto
        product.stock -= quantity
        product.save()
    
    # Limpiar el carrito
    CartItem.objects.all().delete()
    
    return render(request, 'app/payment-success.html', {'order': order})

def payment_failed(request):
    return render(request, 'app/payment-failed.html')







def generate_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Invoice_{order.order_number}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Margins
    margin = 20 * mm

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.setFillColor(colors.black)
    p.drawString(margin, height - margin, "FerreMaX")

    # Company Mission
    p.setFont("Helvetica", 10)
    mission_lines = [
        "Nuestra misión es proporcionar productos de ferretería de alta calidad a precios accesibles,",
        "ofreciendo un servicio excepcional que satisfaga las necesidades de nuestros clientes y contribuya",
        "al desarrollo de nuestras comunidades."
    ]
    p.drawString(margin, height - margin - 20, "Misión de FerreMaX:")
    p.setFont("Helvetica-Oblique", 10)
    y = height - margin - 35
    for line in mission_lines:
        p.drawString(margin, y, line)
        y -= 15

    # Address and RUT
    p.setFont("Helvetica", 10)
    p.drawString(margin, y - 10, "Froilán Roa 7107, 8240000 La Florida")
    p.drawString(margin, y - 25, "Región Metropolitana")
    p.drawString(margin, y - 40, "RUT: 12.345.678-9")

    # Order Information
    p.drawString(margin, y - 70, f"Invoice for Order: {order.order_number}")
    p.drawString(margin, y - 85, f"Date: {order.created_at.strftime('%Y-%m-%d')}")
    p.drawString(margin, y - 100, f"Total: ${order.total_price}")

    y -= 120

    # Separator line
    p.line(margin, y, width - margin, y)
    y -= 10

    # Items
    p.setFont("Helvetica-Bold", 12)
    p.drawString(margin, y, "Cant.")
    p.drawString(margin + 50, y, "Producto")
    p.drawString(width - margin - 100, y, "Precio")
    y -= 15
    p.setFont("Helvetica", 10)
    for item in order.items.all():
        p.drawString(margin, y, str(item.quantity))
        p.drawString(margin + 50, y, item.product.Producto)
        p.drawString(width - margin - 100, y, f"${item.price}")
        y -= 15

    # Separator line
    p.line(margin, y, width - margin, y)
    y -= 10

    # Additional Message
    p.setFont("Helvetica", 10)
    p.drawString(margin, y, "Puedes retirar tu pedido en la tienda de FerreMax más cercana.")

    p.showPage()
    p.save()
    return response




@user_has_role('trabajador', 'administrador','cliente')
@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'app/order_list.html', {'orders': orders})

from django.shortcuts import render, redirect, get_object_or_404
from .forms import StockRequestForm, EditStockForm
from .models import StockRequest, Post

@user_has_role('trabajador', 'administrador')
def stock_request_view(request, product_id):
    producto = get_object_or_404(Post, id=product_id)
    if request.method == 'POST':
        form = StockRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = StockRequestForm(initial={'producto': producto})
    return render(request, 'app/request_form.html', {'form': form, 'producto': producto})

@user_has_role('administrador')
def stock_request_list_view(request):
    requests = StockRequest.objects.all()
    return render(request, 'app/request_list.html', {'requests': requests})

@user_has_role('trabajador', 'administrador')
def inventory_list_view(request):
    productos = Post.objects.all()
    zero_stock_products = productos.filter(stock=0).exists()

    return render(request, 'app/inventory.html', {
        'productos': productos,
        'zero_stock_products': zero_stock_products
    })
    
    


def generate_inventory_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="inventory.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Configurar el margen
    margin = 20 * mm

    # Título y Misión de la Empresa
    p.setFont("Helvetica-Bold", 16)
    p.drawString(margin, height - margin, "FerreMaX")

    # Misión de la Empresa
    p.setFont("Helvetica", 12)
    mission_text = "Nuestra misión es proporcionar productos de ferretería de alta calidad a precios accesibles."
    p.drawString(margin, height - margin - 30, mission_text)

    # Detalles de la Empresa
    p.setFont("Helvetica", 10)
    p.drawString(margin, height - margin - 50, "Froilán Roa 7107, La Florida")
    p.drawString(margin, height - margin - 65, "Región Metropolitana")
    p.drawString(margin, height - margin - 80, "RUT: 12.345.678-9")
    p.drawString(margin, height - margin, "Listado lotes de stock")
    # Espacio antes de la tabla
    y = height - margin - 110

    # Cabecera de la Tabla
    p.setFont("Helvetica-Bold", 12)
    p.drawString(margin, y, "Cant.")
    p.drawString(margin + 50, y, "Producto")
    p.drawString(width - margin - 100, y, "Stock")

    # Listado de productos
    p.setFont("Helvetica", 10)
    productos = Post.objects.all()  # Ajusta la consulta según tu modelo y necesidades
    y -= 20
    for producto in productos:
        p.drawString(margin, y, "1")  # Asumiendo una cantidad estática, ajusta según tus datos
        p.drawString(margin + 50, y, producto.Producto)
        p.drawString(width - margin - 100, y, str(producto.stock))
        y -= 20

        # Agregar una nueva página si es necesario
        if y < margin + 50:
            p.showPage()
            y = height - margin - 140  # Resetear la posición y después de los encabezados

    p.showPage()
    p.save()
    return response


   

def delete_stock_request_view(request, request_id):
    stock_request = get_object_or_404(StockRequest, id=request_id)
    if request.method == 'POST':
        stock_request.delete()
        return redirect('stock_request_list')
    return render(request, 'app/delete_stock_request.html', {'stock_request': stock_request})

def edit_stock_view(request, product_id):
    producto = get_object_or_404(Post, id=product_id)
    if request.method == 'POST':
        form = EditStockForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('stock_request_list')
    else:
        form = EditStockForm(instance=producto)
    return render(request, 'app/edit_stock.html', {'form': form, 'producto': producto})


@user_has_role('trabajador', 'administrador')
@login_required
def all_orders_view(request):
    if not (request.user.is_authenticated and request.user.tipo_de_cuenta in ['trabajador', 'administrador']):
        return redirect('home')

    orders = Order.objects.all()
    query = request.GET.get('query')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if query:
        orders = orders.filter(Q(order_number__icontains=query) | Q(user__username__icontains=query))
    if start_date and end_date:
        orders = orders.filter(created_at__range=[start_date, end_date])

    return render(request, 'app/all_orders.html', {'orders': orders})

@user_has_role('trabajador', 'administrador')
@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'app/order_detail.html', {'order': order})

@user_has_role('administrador')
def most_sold_products_view(request):
    if request.user.is_authenticated and request.user.tipo_de_cuenta == 'administrador':
        most_sold = OrderItem.objects.values('product__Producto', 'product__precio') \
                        .annotate(total_sold=Sum('quantity')) \
                        .order_by('-total_sold')
        return render(request, 'app/most_sold_products.html', {'most_sold': most_sold})
    else:
        return redirect('home')


def generate_most_sold_pdf(request):
    if request.user.is_authenticated and request.user.tipo_de_cuenta == 'administrador':
        most_sold = OrderItem.objects.values('product__Producto', 'product__precio') \
                        .annotate(total_sold=Sum('quantity')) \
                        .order_by('-total_sold')
        top_5_most_sold = most_sold[:5]

        # Crear gráfico de barras
        products = [item['product__Producto'] for item in top_5_most_sold]
        total_sold = [item['total_sold'] for item in top_5_most_sold]

        plt.figure(figsize=(10, 6))
        plt.bar(products, total_sold, color='blue')
        plt.xlabel('Productos')
        plt.ylabel('Total Vendido')
        plt.title('Top 5 Productos Más Vendidos')
        plt.tight_layout()

        # Guardar gráfico en memoria
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()

        # Generar número único y fecha
        report_number = uuid.uuid4().hex[:10].upper()
        current_date = datetime.now().strftime("%Y-%m-%d")

        # Crear el PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="most_sold_products_{report_number}.pdf"'

        p = canvas.Canvas(response, pagesize=letter)
        width, height = letter

        # Encabezado
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, height - 50, "FerreMaX")

        p.setFont("Helvetica", 12)
        p.drawString(100, height - 70, "Nuestra misión es proporcionar productos de ferretería de alta calidad a precios accesibles,")
        p.drawString(100, height - 85, "ofreciendo un servicio excepcional que satisfaga las necesidades de nuestros clientes y contribuya")
        p.drawString(100, height - 100, "al desarrollo de nuestras comunidades.")

        p.drawString(100, height - 130, "Froilán Roa 7107, 8240000 La Florida")
        p.drawString(100, height - 145, "Región Metropolitana")
        p.drawString(100, height - 160, "RUT: 12.345.678-9")

        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, height - 190, "Reporte de Productos Más Vendidos")
        p.setFont("Helvetica", 12)
        p.drawString(100, height - 205, f"Fecha: {current_date}")
        p.drawString(100, height - 220, f"Reporte #: {report_number}")

        # Tabla de productos más vendidos
        p.setFont("Helvetica-Bold", 12)
        y = height - 250
        p.drawString(100, y, "Cant.")
        p.drawString(150, y, "Producto")
        p.drawString(350, y, "Precio")
        p.drawString(450, y, "Total Vendido")
        y -= 20
        p.line(100, y, 500, y)
        y -= 20

        p.setFont("Helvetica", 12)
        for item in most_sold:
            p.drawString(100, y, str(item['total_sold']))
            p.drawString(150, y, item['product__Producto'])
            p.drawString(350, y, f"${item['product__precio']}")
            p.drawString(450, y, str(item['total_sold']))
            y -= 20
            if y < 50:  # Evitar cortar el texto al final de la página
                p.showPage()
                y = height - 100

        # Nueva página para el gráfico
        p.showPage()
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, height - 50, "FerreMaX")
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, height - 70, "Top 5 Productos Más Vendidos")

        # Insertar gráfico en la nueva página
        img = ImageReader(buffer)
        p.drawImage(img, 100, height - 350, width=400, height=300)
        p.save()

        return response
    else:
        return redirect('home')
    
    
    

@user_has_role('administrador')
def proveedor_create_view(request):
    if request.user.is_authenticated and request.user.tipo_de_cuenta == 'administrador':
        if request.method == 'POST':
            form = ProveedorForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('proveedor_list')
        else:
            form = ProveedorForm()
        return render(request, 'app/proveedor_form.html', {'form': form})
    else:
        return redirect('home')

@user_has_role('administrador')
def proveedor_list_view(request):
    if request.user.is_authenticated and request.user.tipo_de_cuenta == 'administrador':
        proveedores = Proveedor.objects.all()
        return render(request, 'app/proveedor_list.html', {'proveedores': proveedores})
    else:
        return redirect('home')    
    
    
    
    
    
# delivery 



@login_required
def add_to_delivery(request, order_id):
    # Configurar PayPal SDK
    paypalrestsdk.configure({
        'mode': 'sandbox',  # Cambiar a 'live' en producción
        'client_id': settings.PAYPAL_CLIENT_ID,
        'client_secret': settings.PAYPAL_CLIENT_SECRET,
    })

    # Obtener la orden
    order = get_object_or_404(Order, id=order_id)

    if order.is_delivery:
        messages.error(request, "Esta orden ya está en delivery.")
        return redirect('order_list')

    # Tarifa de delivery en CLP
    delivery_fee_clp = 5000

    # Obtener la tasa de cambio de CLP a USD
    response = requests.get('https://mindicador.cl/api')
    if response.status_code != 200:
        messages.error(request, "No se pudo obtener la tasa de cambio. Inténtelo de nuevo más tarde.")
        return redirect('order_list')
    
    exchange_rates = response.json()
    clp_to_usd_rate = exchange_rates.get('dolar', {}).get('valor', None)
    if clp_to_usd_rate is None:
        messages.error(request, "No se pudo obtener la tasa de cambio. Inténtelo de nuevo más tarde.")
        return redirect('order_list')

    # Convertir la tarifa de delivery a USD
    delivery_fee_usd = delivery_fee_clp / clp_to_usd_rate

    # Crear el pago en PayPal
    payment = paypalrestsdk.Payment({
        'intent': 'sale',
        'payer': {
            'payment_method': 'paypal'
        },
        'redirect_urls': {
            'return_url': request.build_absolute_uri(reverse('delivery_payment_done', args=[order.id])),
            'cancel_url': request.build_absolute_uri(reverse('delivery_payment_failed')),
        },
        'transactions': [{
            'item_list': {
                'items': [{
                    'name': 'Delivery Fee',
                    'sku': 'delivery',
                    'price': str(round(delivery_fee_usd, 2)),
                    'currency': 'USD',  # Cambiar a USD
                    'quantity': 1,
                }]
            },
            'amount': {
                'total': str(round(delivery_fee_usd, 2)),
                'currency': 'USD'  # Cambiar a USD
            },
            'description': 'Delivery Fee for Order {}'.format(order.order_number)
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == 'approval_url':
                request.session['delivery_order_id'] = order.id
                return redirect(link.href)
    else:
        messages.error(request, f"Error en el pago: {payment.error['message']}")
        return render(request, 'app/delivery_payment_failed.html', {'error': payment.error})

@login_required
def delivery_payment_done(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.is_delivery = True
    order.delivery_status = 'Verificando'
    order.save()
    return render(request, 'app/delivery_payment_success.html', {'order': order})

@login_required
def delivery_payment_failed(request):
    return render(request, 'app/delivery_payment_failed.html')



@login_required
@user_has_role('cliente')
def delivery_tracking(request):
    orders = Order.objects.filter(user=request.user, is_delivery=True)
    return render(request, 'app/delivery_tracking.html', {'orders': orders})


@login_required
@user_has_role('trabajador')
def manage_deliveries(request):
    orders = Order.objects.filter(is_delivery=True)
    return render(request, 'app/manage_deliveries.html', {'orders': orders})


from django.views.decorators.http import require_POST

@require_POST
@user_has_role('trabajador')
@login_required
def update_delivery_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    new_status = request.POST.get('delivery_status')
    if new_status in ['Verificando', 'Enviado', 'Completado']:
        order.delivery_status = new_status
        order.save()
    return redirect('manage_deliveries')


def reportar_fallo(request):
    if request.method == 'POST':
        form = ReporteFalloForm(request.POST, request.FILES)
        if form.is_valid():
            fallo = form.save(commit=False)
            fallo.usuario = request.user
            fallo.save()
            return redirect('home')
    else:
        form = ReporteFalloForm()
    return render(request, 'app/reportar_fallo.html', {'form': form})


@user_has_role('administrador')
@login_required
def ver_fallos(request):
    fallos = Fallo.objects.all()
    return render(request, 'app/ver_fallos.html', {'fallos': fallos})

@user_has_role('administrador')
@login_required
def eliminar_fallo(request, id):
    fallo = Fallo.objects.get(pk=id)
    if request.method == 'POST':
        fallo.delete()
        return HttpResponseRedirect(reverse('ver_fallos'))
    return render(request, 'app/eliminar_fallo.html', {'fallo': fallo})