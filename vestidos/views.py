from django.shortcuts import render, get_object_or_404, redirect
from .forms import VestidoForm
from .models import Vestido
from django.core.paginator import Paginator


def vestidos(request):
    vestidos_disponiveis = Vestido.objects.filter(quantidade_estoque__gt=0)
    paginator = Paginator(vestidos_disponiveis, 15)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'vestidos/vestidos.html', {'vestidos': vestidos_disponiveis, 'page_obj': page_obj})

def adicionar_vestido(request):
    if request.method == 'POST':
        form = VestidoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('administrativo')
    else:
        form = VestidoForm()
    return render(request, 'vestidos/adicionar_vestido.html', {'form': form})


def detalhes_vestido(request, id):
    vestido = get_object_or_404(Vestido, id=id)
    return render(request, 'vestidos/detalhes_vestido.html', {'vestido': vestido})

def editar_vestido(request, id):
    vestido = get_object_or_404(Vestido, id=id)
    if request.method == 'POST':
        form = VestidoForm(request.POST, request.FILES, instance=vestido)
        if form.is_valid():
            form.save()
            return redirect('administrativo')
    else:
        form = VestidoForm(instance=vestido)
    return render(request, 'vestidos/editar_vestido.html', {'form': form})



def excluir_vestido(request, id):
    vestido = get_object_or_404(Vestido, id=id)
    vestido.delete()
    return redirect('administrativo')
