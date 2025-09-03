from django.shortcuts import render, redirect
#-*- coding: utf-8 -*-


from django.http import HttpResponse
from django.template import Template, Context
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import re
from django.core.cache import cache 

# Create your views here.


def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Verificar intentos fallidos
        attempt_key = f'login_attempts_{username}'
        current_attempts = cache.get(attempt_key, 0)
        
        if current_attempts >= 3:
            messages.error(request, 'Cuenta bloqueada. Demasiados intentos fallidos.')
            return render(request, 'iniciar_sesion.html')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Login exitoso - resetear contador
            cache.delete(attempt_key)
            login(request, user)
            return redirect('completo')
        else:
            # Login fallido - incrementar contador
            current_attempts += 1
            cache.set(attempt_key, current_attempts, 300)  # 5 minutos de bloqueo
            
            attempts_left = 3 - current_attempts
            if attempts_left > 0:
                messages.error(request, f'Usuario o contraseña incorrectos. Te quedan {attempts_left} intento(s).')
            else:
                messages.error(request, 'Cuenta bloqueada. Demasiados intentos fallidos.')
    
    return render(request, 'iniciar_sesion.html')

def registro(request):
    print("Método:", request.method)
    if request.method == 'POST':
        print("Datos POST:", request.POST)
        
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Validaciones básicas
        if not all([username, email, password1, password2]):
            messages.error(request, 'Todos los campos son obligatorios')
            return render(request, 'registrarse.html')
        
        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está registrado')
            return render(request, 'registrarse.html')
        
        # Verificar si el email ya existe
        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado')
            return render(request, 'registrarse.html')
        
        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'registrarse.html')
        
        # ✅ NUEVA VALIDACIÓN: Contraseña segura
        if len(password1) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres')
            return render(request, 'registrarse.html')
        
        if not re.search(r'[A-Z]', password1):
            messages.error(request, 'La contraseña debe contener al menos una letra mayúscula')
            return render(request, 'registrarse.html')
        
        if not re.search(r'[0-9]', password1):
            messages.error(request, 'La contraseña debe contener al menos un número')
            return render(request, 'registrarse.html')
        
        # Crear usuario
        try:
            user = User.objects.create_user(username, email, password1)
            user.save()
            
            # Autenticar y loguear automáticamente
            user = authenticate(request, username=username, password=password1)
            if user is not None:
                login(request, user)
                messages.success(request, '¡Usuario creado correctamente!')
                return redirect('inicio')
            else:
                messages.error(request, 'Error en la autenticación')
                
        except Exception as e:
            messages.error(request, f'Error en el registro: {str(e)}')
    
    return render(request, 'registrarse.html')


def inicio(request):
    return render(request, 'inicio.html')

def sesion_iniciada(request):
    return render(request, 'completo.html')