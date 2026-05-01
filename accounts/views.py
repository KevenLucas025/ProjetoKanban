from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import logout
from django.http import JsonResponse
from .models import Card, Profile
from django.contrib import messages
from datetime import datetime,timedelta
import json


def login_view(request):
    if request.method == 'POST':
        usuario_input = request.POST.get('login_user','').strip()
        senha_input = request.POST.get('login_pass','').strip()
        
        
        # 1. Verificação de campos vazios
        if not usuario_input or not senha_input:
            messages.error(request,"Por favor preencha os campos obrigatórios.")
            return render(request, "accounts/login.html")
        
        # 1. Tentar encontrar o objeto do usuário primeiro (por username ou email)
        user_obj = None
        
        # Tenta por username
        user_obj = User.objects.filter(username=usuario_input).first()
        
        # Se não achou por username, tenta por email
        if not user_obj:
            user_obj = User.objects.filter(email=usuario_input).first()
            
        # 2. Se após as duas buscas não achamos ninguém:
        if not user_obj:
            messages.error(request, "Usuário ou e-mail não cadastrados.")
            return render(request, "accounts/login.html")
        
        user = authenticate(request, username=user_obj.username, password=senha_input)
        
        if user is not None:
            login(request,user)
            return redirect("dashboard")
        else:
            # Aqui temos certeza: o usuário existe, mas a senha está errada
            messages.error(request,"Usuário ou senha inválidos.")
            return render(request,"accounts/login.html")
        
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
def mover_card(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            card = Card.objects.get(id=data["id"], user=request.user)
            card.coluna = data["coluna"]
            card.save()

            return JsonResponse({"status": "ok"})
        except Exception as e:
            return JsonResponse({"status": "erro", "msg": str(e)})

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
        
        vencimento = data.get("data_vencimento")
        
        data_vencimento = None
        if vencimento:
            data_vencimento = datetime.strptime(vencimento,"%Y-%m-%d").date()
        else:
            data_vencimento = datetime.today().date() + timedelta(days=5)

        card = Card.objects.create(
            user=request.user,
            titulo=data["titulo"],
            coluna=data["coluna"],
            data_vencimento=data_vencimento
        )
        

        return JsonResponse({
            "id": card.id,
            "titulo": card.titulo,
            "data": card.criado_em.strftime("%d/%m/%Y"),
            "vencimento": card.data_vencimento.strftime("%d/%m/%Y") if card.data_vencimento else "",
            "status": card.status()
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
    vencimento = data.get("data_vencimento")
    
    data_vencimento = None
    if vencimento:
        data_vencimento = datetime.strptime(vencimento, "%Y-%m-%d").date()
    else:
        data_vencimento = datetime.today().date() + timedelta(days=5)

    cards_data = {}

    for coluna in colunas:
        card = Card.objects.create(
            titulo=titulo,
            coluna=coluna,
            user=request.user,
            data_vencimento=data_vencimento
        )

        cards_data[coluna] = {
            "id": card.id,
            "data": card.criado_em.strftime("%d/%m/%Y"),
            "vencimento": card.data_vencimento.strftime("%d/%m/%Y") if card.data_vencimento else "",
            "status": card.status()
        }

    return JsonResponse({
        "status": "ok",
        "titulo": titulo,
        "cards": cards_data
    })
    
    
