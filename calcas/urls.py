from django.urls import path
from calcas.views import calcas, adicionar_calca, editar_calca, excluir_calca, detalhes_calca

urlpatterns = [
    path('calcas/', calcas, name='calcas'),
    path('adicionar_calca/', adicionar_calca, name='adicionar_calca'),
    path('calca/<int:id>/', detalhes_calca, name='detalhes_calca'),
    path('calca/<int:id>/editar/', editar_calca, name='editar_calca'),
    path('calca/<int:id>/excluir/', excluir_calca, name='excluir_calca'),
]
