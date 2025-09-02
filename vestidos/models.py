from django.db import models

class Vestido(models.Model):
    CORES_CHOICES = [
        ('AZ', 'Azul'),
        ('VM', 'Vermelho'),
        ('PR', 'Preto'),
        ('BR', 'Branco'),
        ('AM', 'Amarelo'),
    ]
    
    TAMANHOS_CHOICES = [
        ('PP', 'Extra Pequeno'),
        ('P', 'Pequeno'),
        ('M', 'Médio'),
        ('G', 'Grande'),
        ('GG', 'Extra Grande'),
    ]

    nome = models.CharField('Nome do Produto:', null=False, blank=False, max_length=70)
    preco = models.CharField('Preço:', null=False, blank=False, max_length=10)
    detalhes = models.TextField('Detalhes do Produto:', null=True, blank=True)
    quantidade_estoque = models.IntegerField('Quantidade em Estoque:', default=0)
    cor = models.CharField('Cor:', max_length=2, choices=CORES_CHOICES, default='AZ')
    tamanho = models.CharField('Tamanho:', max_length=2, choices=TAMANHOS_CHOICES, default='M')
    imagem = models.ImageField('Imagem do Produto:', upload_to='produtos/', null=True, blank=True)

    def __str__(self):
        return f'{self.nome}'