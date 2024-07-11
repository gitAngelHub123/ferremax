from django.contrib import admin
from app.models import Post, User

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'Producto', 'categoria', 'precio', 'imagen', 'detalle', 'stock']
    search_fields = ['Producto', 'categoria']
    list_filter = ['categoria']
    
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'nombre', 'apellidos', 'email', 'tipo_de_cuenta', 'is_staff', 'is_active']
    search_fields = ['username', 'nombre', 'apellidos', 'email']
    list_filter = ['tipo_de_cuenta', 'is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('nombre', 'apellidos', 'email')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'nombre', 'apellidos', 'email', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}
        ),
    )
    readonly_fields = ('last_login', 'date_joined')
    
        