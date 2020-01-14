from django.conf.urls import url
from .views import *
from django.urls import include, path
urlpatterns = [
    path('subir-arquivo',enviar_arquivo,name='enviar_arquivo'),
    path('listar-pessoas',pessoa_list,name='pessoas_list'),
    path('registrar_usuario/', registrar_usuario, name='registrar_usuario'),
    path('listar_usuario/', listar_usuario, name='listar_usuario'),

]