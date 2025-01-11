from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from ..forms.auth import CustomUserCreationForm

class RegisterView(CreateView):
    """Vista para registrar nuevos usuarios"""
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, '¡Bienvenido! Tu cuenta ha sido creada exitosamente.')
        return response
        
    def form_invalid(self, form):
        messages.error(self.request, 'Por favor corrige los errores en el formulario.')
        return super().form_invalid(form) 