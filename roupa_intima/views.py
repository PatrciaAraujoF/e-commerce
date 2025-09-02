from django.shortcuts import render, get_object_or_404, redirect
from .forms import RoupaIntimaForm 
from .models import Roupa_intima

def roupas_intimas(request):
    roupas_disponiveis = Roupa_intima.objects.filter(quantidade_estoque__gt=0)
    return render(request, 'roupa_intima/roupas_intimas.html', {'roupas_intimas': roupas_disponiveis})

def adicionar_roupa_intima(request):
    if request.method == 'POST':
        form = RoupaIntimaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('administrativo')
    else:
        form = RoupaIntimaForm()
    return render(request, 'roupa_intima/adicionar_roupa_intima.html', {'form': form})

def detalhes_roupa_intima(request, id):
    roupa_intima = get_object_or_404(Roupa_intima, id=id)
    return render(request, 'roupa_intima/detalhes_roupa_intima.html', {'roupa_intima': roupa_intima})

def editar_roupa_intima(request, id):
    roupa_intima = get_object_or_404(Roupa_intima, id=id)
    if request.method == 'POST':
        form = RoupaIntimaForm(request.POST, request.FILES, instance=roupa_intima)
        if form.is_valid():
            form.save()
            return redirect('administrativo')
    else:
        form = RoupaIntimaForm(instance=roupa_intima)
    return render(request, 'roupa_intima/editar_roupa_intima.html', {'form': form})

def excluir_roupa_intima(request, id):
    roupa_intima = get_object_or_404(Roupa_intima, id=id)
    roupa_intima.delete()
    return redirect('administrativo')
