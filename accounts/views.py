from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import logout
from django.http import JsonResponse
from .models import Card, Profile
from django.contrib import messages
import json


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
        
        nome_completo = request.POST.get('nome_completo','').strip()
        username = request.POST.get('new_user','').strip()
        email = request.POST.get('new_email','').strip()
        password = request.POST.get('new_pass','').strip()
        confirm = request.POST.get('new_confirm','').strip()
        
        if not nome_completo or not username or not email or not password:
            messages.error(request, "Preencha todos os campos")
            return render(request, 'accounts/register.html')

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
            password=password,
            first_name=nome_completo
        )

        messages.success(request, "Conta criada com sucesso")
        return render(request, 'accounts/register.html', {
            'cadastro_ok': True
        })

    return render(request, 'accounts/register.html')

@login_required
@csrf_protect
def upload_foto(request):
    if request.method == "POST" and request.FILES.get("foto"):
        
        profile, created  = Profile.objects.get_or_create(
            user=request.user
        )
        
        profile.foto = request.FILES["foto"]
        profile.save()
    return redirect("dashboard")

@login_required
@csrf_protect
def remover_foto(request):
    if request.method == "POST":

        profile, created = Profile.objects.get_or_create(
            user=request.user
        )

        if profile.foto:
            profile.foto.delete(save=False)
            profile.foto = None
            profile.save()

        return JsonResponse({"status": "ok"})
    
def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def criar_card(request):
    if request.method == "POST":
        data = json.loads(request.body)

        card = Card.objects.create(
            user=request.user,
            titulo=data["titulo"],
            coluna=data["coluna"]
        )
        print("CRIANDO CARD:", data)
        print("CARD SALVO:", card.id)

        return JsonResponse({
            "id": card.id,
            "titulo": card.titulo,
            "data": card.criado_em.strftime("%d/%m/%Y")
        })
        
@login_required   
def renomear_card(request, id):
    if request.method == "POST":
        data = json.loads(request.body)

        card = Card.objects.get(id=id, user=request.user)
        card.titulo = data["titulo"]
        card.save()

        return JsonResponse({"status":"ok"})
    
@login_required   
def excluir_card(request, id):
    if request.method == "POST":
        card = Card.objects.get(id=id, user=request.user)
        card.delete()

        return JsonResponse({"status":"ok"})
    
@login_required
def excluir_lista(request,coluna):
    if request.method == "POST":
        
        Card.objects.filter(
            user=request.user,
            coluna=coluna
        ).delete()
        
    return JsonResponse({"status":"ok"})

@login_required
def criar_card_global(request):

    data = json.loads(request.body)

    titulo = data["titulo"]
    colunas = data["colunas"]

    cards_data = {}

    for coluna in colunas:
        card = Card.objects.create(
            titulo=titulo,
            coluna=coluna,
            user=request.user
        )

        cards_data[coluna] = {
            "id": card.id,
            "data": card.criado_em.strftime("%d/%m/%Y")
        }

    return JsonResponse({
        "status": "ok",
        "titulo": titulo,
        "cards": cards_data
    })
    
    
