import csv,io
from django.shortcuts import render
from .models import *

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
def pessoa_list(request):
    template = 'listar_pessoas.html'
    query = request.GET.get("busca")
    if query:
        pessoa = Arquivo.objects.filter(model__icontais = query).order_by('-notas')
    else:
        pessoa = Arquivo.objects.all().order_by('-notas')
    pessoas = {'lista':pessoa}
    return render(request, template, pessoas)