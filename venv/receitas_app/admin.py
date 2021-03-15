from django.contrib import admin
from .models import Receita

class ListandoReceitas(admin.ModelAdmin):
    list_display = ('id', 'nome_receita', 'categoria')
    list_display_links = ('id', 'nome_receita')

# registra o modelo do app de receitas
admin.site.register(Receita, ListandoReceitas)
