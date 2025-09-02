from django.contrib import admin
from .models import Vestido

class VestidoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'quantidade_estoque', 'cor', 'tamanho')
    list_filter = ('cor', 'tamanho')
    search_fields = ('nome', 'detalhes')

admin.site.register(Vestido, VestidoAdmin)
