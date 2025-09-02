from django.contrib.auth import authenticate, login, logout
from blusas.models import Blusa
from calcas.models import Calca
from vestidos.models import Vestido
from roupa_intima.models import Roupa_intima
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import ItemCarrinho
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from decimal import Decimal, InvalidOperation
from .models import ItemCarrinho, Pedido
import stripe
import logging
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required



def index(request):
    vestidos = Vestido.objects.all()
    blusas = Blusa.objects.all()
    calcas = Calca.objects.all()
    roupas_intimas = Roupa_intima.objects.all()

    paginator_vestidos = Paginator(vestidos, 3)  # 3 cards por página
    paginator_blusas = Paginator(blusas, 3)
    paginator_calcas = Paginator(calcas, 3)
    paginator_roupas_intimas = Paginator(roupas_intimas, 3)

    page_number_vestidos = request.GET.get('page_vestidos')
    page_number_blusas = request.GET.get('page_blusas')
    page_number_calcas = request.GET.get('page_calcas')
    page_number_roupas_intimas = request.GET.get('page_roupas_intimas')

    page_vestidos = paginator_vestidos.get_page(page_number_vestidos)
    page_blusas = paginator_blusas.get_page(page_number_blusas)
    page_calcas = paginator_calcas.get_page(page_number_calcas)
    page_roupas_intimas = paginator_roupas_intimas.get_page(page_number_roupas_intimas)

    context = {
        'page_vestidos': page_vestidos,
        'page_blusas': page_blusas,
        'page_calcas': page_calcas,
        'page_roupas_intimas': page_roupas_intimas,
    }

    return render(request, 'desire_moda_feminina/index.html', context)


def cadastro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.tipo_acesso = 'normal'  
            user.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'desire_moda_feminina/cadastro.html', {'form': form})

def cadastro2(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.tipo_acesso = 'total'  # Define o tipo de acesso
            user.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'desire_moda_feminina/cadastro2.html', {'form': form})




def user_login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redireciona para a página inicial ou dashboard após login
            else:
                form.add_error(None, 'Credenciais inválidas')
    else:
        form = CustomAuthenticationForm()
        
    return render(request, 'desire_moda_feminina/login.html', {'form': form})



def dashboard(request):
    return render(request, 'desire_moda_feminina/dashboard.html')


def administrativo(request):
    return render(request, 'desire_moda_feminina/administrativo.html')


def vestidos_adm(request):
    vestidos_disponiveis = Vestido.objects.filter(quantidade_estoque__gt=0)
    return render(request, 'desire_moda_feminina/vestidos_adm.html', {'vestidos': vestidos_disponiveis})

def blusas_adm(request):
    blusas_disponiveis = Blusa.objects.filter(quantidade_estoque__gt=0)
    return render(request, 'desire_moda_feminina/blusas_adm.html', {'blusas': blusas_disponiveis})


def calcas_adm(request):
    calcas_disponiveis = Calca.objects.filter(quantidade_estoque__gt=0)
    return render(request, 'desire_moda_feminina/calcas_adm.html', {'calcas': calcas_disponiveis})

def ri_adm(request):
    ri_disponiveis = Roupa_intima.objects.filter(quantidade_estoque__gt=0)
    return render(request, 'desire_moda_feminina/ri_adm.html', {'ri': ri_disponiveis})


def user_logout_view(request):
    logout(request)
    return redirect('index')  



#carrinho


@login_required
def adicionar_ao_carrinho(request, produto_id, produto_tipo):
    if request.user.is_authenticated:
        item_carrinho, created = ItemCarrinho.objects.get_or_create(
            user=request.user,
            produto_id=produto_id,
            produto_tipo=produto_tipo,
            defaults={'quantidade': 1}
        )
        if not created:
            item_carrinho.quantidade += 1
            item_carrinho.save()
    else:
        return redirect('login')
    
    return redirect('carrinho')
@login_required
def visualizar_carrinho(request):
    itens_carrinho = ItemCarrinho.objects.filter(user=request.user)
    
    for item in itens_carrinho:
        if item.produto_tipo == 'Roupa_intima':
            item.produto = Roupa_intima.objects.get(id=item.produto_id)
        elif item.produto_tipo == 'Vestido':
            item.produto = Vestido.objects.get(id=item.produto_id)
        elif item.produto_tipo == 'Blusa':
            item.produto = Blusa.objects.get(id=item.produto_id)
        elif item.produto_tipo == 'Calca':
            item.produto = Calca.objects.get(id=item.produto_id)
    
    return render(request, 'desire_moda_feminina/carrinho.html', {'itens_carrinho': itens_carrinho})

@login_required
def remover_do_carrinho(request, item_id):
    item = get_object_or_404(ItemCarrinho, id=item_id, user=request.user)
    item.delete()
    return redirect('carrinho')

@login_required
def atualizar_quantidade(request, item_id):
    if request.method == 'POST':
        quantidade = int(request.POST.get('quantidade', 1))
        if quantidade > 0:
            item = get_object_or_404(ItemCarrinho, id=item_id, user=request.user)
            item.quantidade = quantidade
            item.save()
    return redirect('carrinho')





stripe.api_key = settings.STRIPE_SECRET_KEY

logger = logging.getLogger(__name__)

@login_required
def finalizar_compra(request):
    logger.info("Iniciando a finalização da compra...")

    itens_carrinho = ItemCarrinho.objects.filter(user=request.user)
    total = Decimal('0.00')
    logger.info(f"Número de itens no carrinho: {itens_carrinho.count()}")

    for item in itens_carrinho:
        try:
            if item.produto_tipo == 'Roupa_intima':
                produto = Roupa_intima.objects.get(id=item.produto_id)
            elif item.produto_tipo == 'Vestido':
                produto = Vestido.objects.get(id=item.produto_id)
            elif item.produto_tipo == 'Blusa':
                produto = Blusa.objects.get(id=item.produto_id)
            elif item.produto_tipo == 'Calca':
                produto = Calca.objects.get(id=item.produto_id)

            preco = Decimal(produto.preco)
            total += preco * item.quantidade
        except InvalidOperation:
            logger.error("Erro ao processar o preço do produto.")
            return render(request, 'desire_moda_feminina/erro_formatacao.html', {'mensagem': 'Erro ao processar o preço do produto.'})

    logger.info(f"Total calculado para o pedido: {total}")

    total_cents = int(total * 100) 
    logger.info(f"Total em centavos: {total_cents}")

    if request.method == 'POST':
        logger.info("Processando pagamento com Stripe...")
        try:
            stripe_token = request.POST.get('stripeToken')
            print(f"Stripe Token recebido: {stripe_token}")

          
            if stripe_token is None:
                logger.error("Stripe Token não fornecido.")
                return render(request, 'erro_pagamento.html', {'mensagem': 'Erro: Stripe token não recebido.'})

            charge = stripe.Charge.create(
                amount=total_cents,
                currency='brl',
                description='Compra em Desire Moda Feminina',
                source=stripe_token
            )
            logger.info("Pagamento realizado com sucesso!")
            print("Pagamento realizado com sucesso!")

            pedido = Pedido.objects.create(user=request.user, total=total, status='Pago')
            logger.info(f"Pedido {pedido.id} criado com sucesso.")
            itens_carrinho.delete()
            return redirect('confirmacao_compra')
        except stripe.error.StripeError as e:
            logger.error(f"Erro no pagamento com Stripe: {e}")
            return render(request, 'erro_pagamento.html', {'mensagem': str(e)})

    return render(request, 'desire_moda_feminina/finalizacao_compra.html', {'itens_carrinho': itens_carrinho, 'total': total, 'stripe_public_key': settings.STRIPE_PUBLIC_KEY})



@login_required
def confirmacao_compra(request):
    return render(request, 'desire_moda_feminina/confirmacao_compra.html')


@login_required
def acompanhar_pedidos(request):
    pedidos = Pedido.objects.filter(user=request.user).order_by('-data_criacao')
    return render(request, 'desire_moda_feminina/acompanhamento_pedidos.html', {'pedidos': pedidos})

def erro_formatacao(request, mensagem):
    return render(request, 'desire_moda_feminina/erro_formatacao.html', {'mensagem': mensagem})


#-------------TESTE



stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def pagina_finalizacao(request):
  
    stripe_public_key = settings.STRIPE_PUBLIC_KEY or 'chave-padrao-para-desenvolvimento'
    context = {
        'STRIPE_PUBLIC_KEY': stripe_public_key,
    }
    return render(request, 'desire_moda_feminina/finalizacao_compra.html', context)


@login_required
def finalizar_compra(request):
    # Log para depuração
    print("Iniciando a finalização da compra...")

    # Obter os itens do carrinho do usuário atual
    itens_carrinho = ItemCarrinho.objects.filter(user=request.user)
    total = Decimal('0.00')
    print(f"Número de itens no carrinho: {itens_carrinho.count()}")

    itens_detalhes = []  # Lista para armazenar detalhes dos itens do carrinho

    for item in itens_carrinho:
        try:
            if item.produto_tipo == 'Roupa_intima':
                produto = Roupa_intima.objects.get(id=item.produto_id)
            elif item.produto_tipo == 'Vestido':
                produto = Vestido.objects.get(id=item.produto_id)
            elif item.produto_tipo == 'Blusa':
                produto = Blusa.objects.get(id=item.produto_id)
            elif item.produto_tipo == 'Calca':
                produto = Calca.objects.get(id=item.produto_id)

            preco = Decimal(produto.preco)
            total += preco * item.quantidade

            # Adicionar detalhes do produto à lista
            itens_detalhes.append({
                'nome': produto.nome,
                'quantidade': item.quantidade,
                'preco': preco,
            })

        except Exception as e:
            print("Erro ao processar o preço do produto:", e)
            return render(request, 'desire_moda_feminina/erro_formatacao.html', {'mensagem': 'Erro ao processar o preço do produto.'})

    print(f"Total calculado para o pedido: {total}")

    total_cents = int(total * 100)  
    print(f"Total em centavos: {total_cents}")

    if request.method == 'POST':
        print("Processando pagamento com Stripe...")
        try:
            stripe_token = request.POST.get('stripeToken')
            print(f"Stripe Token recebido: {stripe_token}")

            if stripe_token is None:
                print("Stripe Token não fornecido.")
                return render(request, 'desire_moda_feminina/erro_pagamento.html', {'mensagem': 'Erro: Stripe token não recebido.'})

            # Criar o pagamento
            charge = stripe.Charge.create(
                amount=total_cents,
                currency='brl',
                description='Compra em Desire Moda Feminina',
                source=stripe_token
            )
            print("Pagamento realizado com sucesso!")

            pedido = Pedido.objects.create(user=request.user, total=total, status='Pago')
            print(f"Pedido {pedido.id} criado com sucesso.")
            itens_carrinho.delete()
            return redirect('confirmacao_compra')
        except stripe.error.StripeError as e:
            print(f"Erro no pagamento com Stripe: {e}")
            return render(request, 'desire_moda_feminina/erro_pagamento.html', {'mensagem': str(e)})

    return render(request, 'desire_moda_feminina/finalizacao_compra.html', {
        'itens_carrinho': itens_carrinho,
        'total': total,
        'itens_detalhes': itens_detalhes,  
        'usuario': request.user.nome, 
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })




@login_required
def processar_pagamento(request):
    if request.method == 'POST':
        print("Processamento de pagamento iniciado.")
        try:
            
            total = Decimal('78.00')  
            total_cents = int(total * 100)

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'brl',
                        'product_data': {
                            'name': 'Produtos no carrinho',
                        },
                        'unit_amount': total_cents,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/confirmacao_compra/'),
                cancel_url=request.build_absolute_uri('/erro_formatacao/'),
            )
            print("Sessão de pagamento criada com sucesso:", session.id)
            return JsonResponse({'id': session.id})
        except Exception as e:
            print("Erro ao criar sessão de pagamento:", str(e))
            return JsonResponse({'error': str(e)}, status=400)

    print("Método não permitido:", request.method)
    return JsonResponse({'status': 'método não permitido'}, status=405)