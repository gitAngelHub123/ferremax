from django.db import models
from django.conf import settings


from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.contrib.auth.models import AbstractUser, Group, Permission

from django.utils.translation import gettext_lazy as _



class Post(models.Model):
    Producto = models.CharField(max_length=50)
    categoria = models.CharField(max_length=50)
    precio = models.IntegerField()  # Agregar los paréntesis
    imagen = models.ImageField(upload_to='images/')# Agregar los paréntesis y el parámetro upload_to
    detalle = models.TextField()
    stock = models.IntegerField()
    def __str__(self):
        return self.Producto
    
    
class CartItem(models.Model):
    product = models.ForeignKey(Post, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.product.Producto}'

    def get_total_price(self):
        return self.quantity * self.product.precio    

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    order_number = models.CharField(max_length=20, unique=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    direccion = models.CharField(max_length=255)
    is_delivery = models.BooleanField(default=False)  # Nuevo campo para indicar si es delivery
    delivery_status = models.CharField(max_length=50, default='Pending')  # Nuevo campo para el estado del delivery

    def __str__(self):
        return f"Order {self.order_number}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Post, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.Producto}"

class User(AbstractUser):
    TIPO_DE_CUENTA_CHOICES = [
        ('administrador', 'Administrador'),
        ('cliente', 'Cliente'),
        ('trabajador', 'Trabajador'),
    ]

    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    tipo_de_cuenta = models.CharField(max_length=20, choices=TIPO_DE_CUENTA_CHOICES)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    imagen_perfil = models.ImageField(upload_to='imagenes_perfil/', blank=True, null=True)

    groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, verbose_name=_('user permissions'), blank=True, related_name='custom_user_set')

    def __str__(self):
        return self.username
    
class SolicitudArticulo(models.Model):
    numeroSolicitud = models.AutoField(primary_key=True)
    nombreUsuario = models.CharField(max_length=50)
    solicitud = models.TextField()

    def __str__(self):
        return self.solicitud
    
    
class StockRequest(models.Model):
    producto = models.ForeignKey(Post, on_delete=models.CASCADE)
    cantidad_necesaria = models.IntegerField()
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.producto.Producto} - {self.cantidad_necesaria} unidades"
    
    
class Proveedor(models.Model):
    nombre_empresa = models.CharField(max_length=100)
    numero_telefono = models.CharField(max_length=15)
    correo = models.CharField(max_length=100)
    
    ESPECIALIDAD_CHOICES = [
        ('materiales', 'Materiales'),
        ('herramientas_manuales', 'Herramientas Manuales'),
        ('herramientas_electricas', 'Herramientas Eléctricas'),
        ('herramientas_seguridad', 'Herramientas de Seguridad'),
    ]
    especialidad = models.CharField(max_length=30, choices=ESPECIALIDAD_CHOICES)

    def __str__(self):
        return self.nombre_empresa    
    
    
    
class Fallo(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fallos')
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=100, blank=True)
    imagen = models.ImageField(upload_to='fallos/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=100, default='pendiente')

    def __str__(self):
        return self.titulo    