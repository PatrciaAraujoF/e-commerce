from django.urls import path
from blusas.views import blusas, adicionar_blusa, editar_blusa, excluir_blusa, detalhes_blusa

urlpatterns = [
    path('blusas/', blusas, name='blusas'),
    path('adicionar_blusa/', adicionar_blusa, name='adicionar_blusa'),
    path('blusa/<int:id>/', detalhes_blusa, name='detalhes_blusa'),
    path('blusa/<int:id>/editar/', editar_blusa, name='editar_blusa'),
    path('blusa/<int:id>/excluir/', excluir_blusa, name='excluir_blusa'),
]
