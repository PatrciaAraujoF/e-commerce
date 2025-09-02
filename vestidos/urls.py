from django.urls import path
from vestidos.views import vestidos, adicionar_vestido, editar_vestido, excluir_vestido, detalhes_vestido

urlpatterns = [
    path('vestidos/', vestidos, name='vestidos'),
    path('adicionar_vestido/', adicionar_vestido, name='adicionar_vestido'),
    path('vestido/<int:id>/', detalhes_vestido, name='detalhes_vestido'),
    path('vestido/<int:id>/editar/', editar_vestido, name='editar_vestido'),
    path('vestido/<int:id>/excluir/', excluir_vestido, name='excluir_vestido'),
]
