"""
Views para autenticação e gerenciamento de usuários.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages

from ..forms import UserRegistrationForm


def register_view(request):
    """View para registro de novos usuários"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'identity/register.html', {'form': form})
