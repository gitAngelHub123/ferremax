from django.urls import path, include
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('base/', base, name='base'),
    path('buscar/', buscar, name='buscar'),
    # Registrar Usuario
    path('registro/', registro_cliente, name='registro'),
    path('registro_administrador/', registro_administrador, name='registro_administrador'),
    path('registro_trabajador/', registro_trabajador, name='registro_trabajador'),
    path('editar-usuario/', editar_usuario, name='editar_usuario'),
    path('perfil/', perfil_usuario, name='perfil_usuario'),
    path('cambiar-contrasena/', cambiar_contrasena, name='cambiar_contrasena'),
    path('recuperar-contrasena/', recuperar_contrasena, name='recuperar_contrasena'),
    # Iniciar sesión
    path('inicio_sesion/', inicio_sesion, name='inicio_sesion'),
    path('cerrar_sesion/', cerrar_sesion, name='cerrar_sesion'),
    # Artículo
    path('solicitarArticulo/', solicitud_articulo, name='solicitar_articulo'),
    path('solicitud-exitosa/', solicitud_exitosa, name='solicitud_exitosa'),
    path('solicitudes/', listar_solicitudes, name='listar_solicitudes'),
    path('eliminar/<int:numero_solicitud>/', eliminar_solicitud, name='eliminar_solicitud'),
    # Carrito
    path('productos/', product_list, name='product_list'),  # URL para product_list
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_detail, name='cart_detail'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    # PayPal
    path('process-payment/', process_payment, name='process_payment'),
    path('payment-done/', payment_done, name='payment_done'),
    path('payment-failed/', payment_failed, name='payment_failed'),
    path('invoice/<int:order_id>/', generate_invoice, name='generate_invoice'),
    path('orders/', order_list, name='order_list'),
    path('all-orders/', all_orders_view, name='all_orders'),
    path('order/<int:order_id>/', order_detail_view, name='order_detail'),
    path('most-sold-products/', most_sold_products_view, name='most_sold_products'),
    path('generate-most-sold-pdf/', generate_most_sold_pdf, name='generate_most_sold_pdf'), 
    path('request/<int:product_id>/', stock_request_view, name='stock_request'),
    path('requests/', stock_request_list_view, name='stock_request_list'),
    path('inventory/', inventory_list_view, name='inventory_list'),
    path('inventory/pdf/', generate_inventory_pdf, name='inventory_pdf'),
    path('requests/delete/<int:request_id>/', delete_stock_request_view, name='delete_stock_request'),
    path('requests/edit_stock/<int:product_id>/', edit_stock_view, name='edit_stock'),
    path('proveedor/add/', proveedor_create_view, name='proveedor_add'),
    path('proveedores/', proveedor_list_view, name='proveedor_list'),
    
    #delivery
    path('add-to-delivery/<int:order_id>/', add_to_delivery, name='add_to_delivery'),
    path('delivery-payment-done/<int:order_id>/', delivery_payment_done, name='delivery_payment_done'),
    path('delivery-payment-failed/', delivery_payment_failed, name='delivery_payment_failed'),
    path('delivery-tracking/', delivery_tracking, name='delivery_tracking'),
    path('manage-deliveries/', manage_deliveries, name='manage_deliveries'),
    path('update-delivery-status/<int:order_id>/', update_delivery_status, name='update_delivery_status'),
    
    #FALLO
    path('reportar-fallo/', reportar_fallo, name='reportar_fallo'),
    path('ver-fallos/', ver_fallos, name='ver_fallos'),
    path('eliminar-fallo/<int:id>/', eliminar_fallo, name='eliminar_fallo'),
]