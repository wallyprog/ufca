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
def listar_usuario(request, template_name="listar.html"):
    usuarios = User.objects.all()
    usuario = {'lista': usuarios}
    return render(request, template_name, usuario)

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