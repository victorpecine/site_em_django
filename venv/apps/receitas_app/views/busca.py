from receitas_app.models import Receita
from django.shortcuts import render, get_object_or_404, redirect


# configurando a busca da index
def busca(request):
    """Faz a busca de receitas no sistema"""
    lista_receitas = Receita.objects.order_by('-data_receita').filter(receita_publicada=True)
    if 'buscar' in request.GET:
        nome_a_buscar = request.GET['buscar']
        lista_receitas = lista_receitas.filter(nome_receita__icontains=nome_a_buscar)
    dados = {'receitas': lista_receitas}
    return render(request, 'receitas/buscar.html', dados)
