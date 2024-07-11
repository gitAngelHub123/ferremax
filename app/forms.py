from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import User, SolicitudArticulo, StockRequest, Post, Proveedor,Fallo
from django.contrib.auth import get_user_model

User = get_user_model()

class RecuperarContrasenaForm(forms.Form):
    username = forms.CharField(max_length=150, label='Nombre de usuario')
    nombre = forms.CharField(max_length=100, label='Nombre')
    apellidos = forms.CharField(max_length=100, label='Apellidos')

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = 'Contraseña actual'
        self.fields['new_password1'].label = 'Nueva contraseña'
        self.fields['new_password2'].label = 'Confirmar nueva contraseña'

    old_password = forms.CharField(label='Contraseña actual', widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}))
    new_password1 = forms.CharField(label='Nueva contraseña', widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    new_password2 = forms.CharField(label='Confirmar nueva contraseña', widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))


class RegistroClienteForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['nombre', 'apellidos', 'username', 'password1', 'password2', 'tipo_de_cuenta', 'direccion', 'imagen_perfil']
        widgets = {
            'tipo_de_cuenta': forms.HiddenInput(attrs={'value': 'cliente'})
        }

class RegistroAdministradorForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['nombre', 'apellidos', 'username', 'password1', 'password2', 'tipo_de_cuenta', 'direccion', 'imagen_perfil']
        widgets = {
            'tipo_de_cuenta': forms.HiddenInput(attrs={'value': 'administrador'})
        }

class RegistroTrabajadorForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['nombre', 'apellidos', 'username', 'password1', 'password2', 'tipo_de_cuenta', 'direccion', 'imagen_perfil']
        widgets = {
            'tipo_de_cuenta': forms.HiddenInput(attrs={'value': 'trabajador'})
        }
 
 
class EditarUsuarioForm(UserChangeForm):
    password = None  # No necesitamos la contraseña en el formulario de edición

    class Meta:
        model = User
        fields = ['nombre', 'apellidos', 'username', 'direccion', 'imagen_perfil'] 
 
        
class InicioSesionForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    
class SolicitudArticuloForm(forms.ModelForm):
    class Meta:
        model = SolicitudArticulo
        fields = '__all__'  
        
        
        

class StockRequestForm(forms.ModelForm):
    class Meta:
        model = StockRequest
        fields = ['producto', 'cantidad_necesaria']
        widgets = {
            'producto': forms.HiddenInput()
        }

class EditStockForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['stock']
        
class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre_empresa', 'numero_telefono','correo', 'especialidad']        
        
        
        
        

class ReporteFalloForm(forms.ModelForm):
    class Meta:
        model = Fallo
        fields = ['titulo', 'descripcion', 'categoria', 'imagen']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }        