from django.shortcuts import render, get_object_or_404, redirect
from .forms import CalcaForm 
from .models import Calca

def calcas(request):
    calcas_disponiveis = Calca.objects.filter(quantidade_estoque__gt=0)
    return render(request, 'calcas/calcas.html', {'calcas': calcas_disponiveis})

def adicionar_calca(request):
    if request.method == 'POST':
        form = CalcaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('administrativo')
    else:
        form = CalcaForm()
    return render(request, 'calcas/adicionar_calca.html', {'form': form})

def detalhes_calca(request, id):
    calca = get_object_or_404(Calca, id=id)
    return render(request, 'calcas/detalhes_calca.html', {'calca': calca})

def editar_calca(request, id):
    calca = get_object_or_404(Calca, id=id)
    if request.method == 'POST':
        form = CalcaForm(request.POST, request.FILES, instance=calca)
        if form.is_valid():
            form.save()
            return redirect('administrativo')
    else:
        form = CalcaForm(instance=calca)
    return render(request, 'calcas/editar_calca.html', {'form': form})

def excluir_calca(request, id):
    calca = get_object_or_404(Calca, id=id)
    calca.delete()
    return redirect('administrativo')
