from django.contrib import admin
from .models import Pessoa


class ListandoPessoas(admin.ModelAdmin):
    list_display = ('id', 'nome_pessoa', 'email')
    list_display_links = ('id', 'nome_pessoa', 'email')
    search_fields = ('nome_pessoa', 'email')
    list_filter = ('nome_pessoa',)
    list_per_page = 20

admin.site.register(Pessoa, ListandoPessoas)