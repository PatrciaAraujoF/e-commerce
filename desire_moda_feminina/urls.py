from django.urls import path
from . import views
from .views import user_login_view, user_logout_view 
from django.http import HttpResponse 

urlpatterns = [
    path('', views.index, name='index'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('cadastro2/', views.cadastro2, name='cadastro2'),
    path('login/', user_login_view, name='login'),  
    path('logout/', user_logout_view, name='logout'), 
    path('dashboard/', views.dashboard, name='dashboard'),
    path('administrativo/', views.administrativo, name='administrativo'),

    path('vestidos/administrativo/', views.vestidos_adm, name='vestidos_adm'),
    path('blusas/administrativo/', views.blusas_adm, name='blusas_adm'),
    path('calcas/administrativo/', views.calcas_adm, name='calcas_adm'),
    path('roupas-intimas/administrativo/', views.ri_adm, name='ri_adm'),
    
    
    path('carrinho/adicionar/<int:produto_id>/<str:produto_tipo>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('carrinho/', views.visualizar_carrinho, name='carrinho'),
    path('carrinho/remover/<int:item_id>/', views.remover_do_carrinho, name='remover_do_carrinho'),
    path('carrinho/atualizar/<int:item_id>/', views.atualizar_quantidade, name='atualizar_quantidade'),

    path('carrinho/finalizar/', views.finalizar_compra, name='finalizar_compra'),
    path('confirmacao_compra/', views.confirmacao_compra, name='confirmacao_compra'),
    path('pedidos/', views.acompanhar_pedidos, name='acompanhar_pedidos'),
    path('erro_formatacao/<str:mensagem>/', views.erro_formatacao, name='erro_formatacao'),



    path('finalizacao-compra/', views.pagina_finalizacao, name='finalizacao_compra'),
    path('processar-pagamento/', views.processar_pagamento, name='processar_pagamento'),
    path('carrinho/finalizar/', views.finalizar_compra, name='finalizar_compra'),

]
