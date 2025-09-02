from django import forms
from .models import Roupa_intima



class RoupaIntimaForm(forms.ModelForm):
    class Meta:
        model = Roupa_intima
        fields = ['nome', 'preco', 'detalhes', 'cor', 'tamanho', 'imagem', 'quantidade_estoque']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Produto'}),
            'preco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Preço'}),
            'detalhes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Detalhes do Produto'}),
            'cor': forms.Select(attrs={'class': 'form-select'}),
            'tamanho': forms.Select(attrs={'class': 'form-select'}),
            'quantidade_estoque': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade em Estoque'}),
        }