from django.conf.urls import url
from .views import *
from django.urls import include, path
urlpatterns = [
    path('subir-arquivo',enviar_arquivo,name='enviar_arquivo')
]