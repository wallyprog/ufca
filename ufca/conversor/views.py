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
            descricao = collumn[2]
        )
    context = {}
    return render(request,template, context)
