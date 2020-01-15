import csv,io
from django.shortcuts import render, redirect
from .models import *
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseRedirect

@login_required
def registrar_usuario(request, template_name="registrar.html"):
    user = request.user
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        tipo = request.POST['tipo_usuario']
        if tipo == "administrador":
            user = User.objects.create_user(username, email, password)
            user.is_staff = True
            user.save()
        else:
            user = User.objects.create_user(username, email, password)

        return redirect('/listar_usuario/') 
    return render(request, template_name, {})
@login_required
def listar_usuario(request, template_name="listar.html"):
    usuarios = User.objects.all()
    usuario = {'lista': usuarios}
    return render(request, template_name, usuario)

def logar_usuario(request, template_name='login.html'):
    next = request.GET.get('next','listar_usuario')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(next)
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
            return HttpResponseRedirect(settings.LOGIN_URL)
    return render(request, template_name, {'redirect_to': next})
@login_required
def deletar_usuario(request, pk, template_name='delete.html'):
    user = request.user
    if user.has_perm('user.delete_user'):
        try:
            usuario = User.objects.get(pk=pk)
            if request.method == 'POST':
                usuario.delete()
                return redirect('listar_usuario')
        except:
            messages.error(request,'Usuario não encontrado')
            return redirect('listar_usuario')
    else:
        messages.error(request,'Permissão negada')
        return redirect('listar_usuario')
    return render(request,template_name,{'usuario':usuario})

def deslogar(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)
@login_required
def enviar_arquivo(request):
    template = 'subir_arquivo.html'
    if request.method == 'GET':
        return render(request,template)
    csv_file = request.FILES['file']
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for collumn in csv.reader(io_string, delimiter = ",",quotechar="|"):
        _, created = Arquivo.objects.update_or_create(
            nome = collumn[0],
            endereco = collumn[1],
            descricao = collumn[2],
            notas = collumn[3]
        )
    context = {}
    return render(request,template, context)

@login_required
def pessoa_list(request):
    template = 'listar_pessoas.html'
    query = request.GET.get("busca")
    if query:
        pessoa = Arquivo.objects.filter(model__icontais = query).order_by('-notas')
    else:
        pessoa = Arquivo.objects.all().order_by('-notas')
    pessoas = {'lista':pessoa}
    return render(request, template, pessoas)