from django.shortcuts import render, get_object_or_404, redirect
from blusas.forms import BlusaForm
from .models import Blusa  

def blusas(request):
    blusas_disponiveis = Blusa.objects.filter(quantidade_estoque__gt=0)
    return render(request, 'blusas/blusas.html', {'blusas': blusas_disponiveis})

def adicionar_blusa(request):
    if request.method == 'POST':
        form = BlusaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('administrativo')
    else:
        form = BlusaForm()
    return render(request, 'blusas/adicionar_blusa.html', {'form': form})

def detalhes_blusa(request, id):
    blusa = get_object_or_404(Blusa, id=id)
    return render(request, 'blusas/detalhes_blusa.html', {'blusa': blusa})

def editar_blusa(request, id):
    blusa = get_object_or_404(Blusa, id=id)
    if request.method == 'POST':
        form = BlusaForm(request.POST, request.FILES, instance=blusa)
        if form.is_valid():
            form.save()
            return redirect('administrativo')
    else:
        form = BlusaForm(instance=blusa)
    return render(request, 'blusas/editar_blusa.html', {'form': form})

def excluir_blusa(request, id):
    blusa = get_object_or_404(Blusa, id=id)
    blusa.delete()
    return redirect('administrativo')
