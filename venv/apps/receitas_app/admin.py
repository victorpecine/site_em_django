from django.contrib import admin
from .models import Receita

class ListandoReceitas(admin.ModelAdmin):
    list_display = ('id', 'nome_receita', 'autor', 'categoria', 'receita_publicada', 'data_receita')
    list_display_links = ('id', 'nome_receita')
    search_fields = ('nome_receita',)
    list_filter = ('categoria',)
    list_editable = ('receita_publicada',)
    list_per_page = 20

# registra o modelo do app de receitas
admin.site.register(Receita, ListandoReceitas)
