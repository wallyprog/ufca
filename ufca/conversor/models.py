from django.db import models

class Arquivo(models.Model):
    nome = models.CharField(max_length = 50,null = False)
    endereco = models.CharField(max_length = 50 , null= False)
    descricao = models.TextField(max_length = 100 , null = False)
