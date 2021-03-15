from django.shortcuts import render, get_object_or_404
from .models import Receita

def index(request):
    # mostrando na página as receitas em ordem da mais nova para a mais antiga e apenas as publicadas
    receitas = Receita.objects.order_by('-data_receita').filter(receita_publicada=True)
    dados = {'receitas': receitas}
    return render(request, 'index.html', dados)

def receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id) # obtendo a receita a partir do index no BD
    receita_a_exibir = {'receita': receita}
    return render(request, 'receita.html', receita_a_exibir)

# configurando a busca da index
def buscar(request):
    lista_receitas = Receita.objects.order_by('-data_receita').filter(receita_publicada=True)
    if 'buscar' in request.GET:
        nome_a_buscar = request.GET['buscar']
        if buscar:
            lista_receitas = lista_receitas.filter(nome_receita__icontains=nome_a_buscar)
    dados = {'receitas': lista_receitas}
    return render(request, 'buscar.html', dados)
