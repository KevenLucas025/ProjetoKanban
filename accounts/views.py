from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
        usuario = request.POST.get('login_user')
        senha = request.POST.get('login_pass')
        
        print("USER INPUT:", usuario)
        print("PASS INPUT:", senha)
        
        user = authenticate(request, username=usuario, password=senha)
        
        print("AUTH RESULT:", user)
        
        if user is None:
            try:
                usuario_obj = User.objects.get(email=usuario)
                
                user = authenticate(
                    request,
                    username=usuario_obj.username,
                    password=senha
                )
            except User.DoesNotExist:
                pass
        if user:
            login(request,user)
            return redirect('dashboard')
        
        messages.error(request, "Usuário ou senha inválidos")
        
    return render(request, 'accounts/login.html')


def register_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')

        if password != confirm:
            messages.error(request, "As senhas não coincidem")
            return render(request, 'accounts/register.html',{
                'erro_campo':'senha'
            })

        if User.objects.filter(username=username).exists():
            messages.error(request, "Usuário já existe")
            return render(request, 'accounts/register.html',{
                'erro_campo': 'username'
            })
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email já cadastrado')
            return render(request, 'accounts/register.html', {
                'erro_campo': 'email'
            })

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Conta criada com sucesso")
        return render(request, 'accounts/register.html', {
            'cadastro_ok': True
        })

    return render(request, 'accounts/register.html')