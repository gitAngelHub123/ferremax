from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseForbidden

def user_has_role(*roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.tipo_de_cuenta in roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
        return _wrapped_view
    return decorator

def redirect_authenticated_user(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')  # Redirigir a la página principal o cualquier otra página
        return view_func(request, *args, **kwargs)
    return _wrapped_view