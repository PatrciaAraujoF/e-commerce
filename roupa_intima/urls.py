from django.urls import path
from roupa_intima.views import roupas_intimas, adicionar_roupa_intima, editar_roupa_intima, excluir_roupa_intima, detalhes_roupa_intima

urlpatterns = [
    path('roupas_intimas/', roupas_intimas, name='roupas_intimas'),
    path('adicionar_roupa_intima/', adicionar_roupa_intima, name='adicionar_roupa_intima'),
    path('roupa_intima/<int:id>/', detalhes_roupa_intima, name='detalhes_roupa_intima'),
    path('roupa_intima/<int:id>/editar/', editar_roupa_intima, name='editar_roupa_intima'),
    path('roupa_intima/<int:id>/excluir/', excluir_roupa_intima, name='excluir_roupa_intima'),
]
