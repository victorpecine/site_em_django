from django.shortcuts import render, get_object_or_404, redirect
from .models import Receita
from django.contrib.auth.models import User
from django.contrib import auth, messages


def index(request):
    # mostrando na página as receitas em ordem da mais nova para a mais antiga e apenas
    # as publicadas
    receitas = Receita.objects.order_by('-data_receita').filter(receita_publicada=True)
    dados = {'receitas': receitas}
    return render(request, 'receitas/index.html', dados)


def receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)  # obtendo a receita a partir do index no BD
    receita_a_exibir = {'receita': receita}
    return render(request, 'receitas/receita.html', receita_a_exibir)


# configurando a busca da index
def buscar(request):
    lista_receitas = Receita.objects.order_by('-data_receita').filter(receita_publicada=True)
    if 'buscar' in request.GET:
        nome_a_buscar = request.GET['buscar']
        if buscar:
            lista_receitas = lista_receitas.filter(nome_receita__icontains=nome_a_buscar)
    dados = {'receitas': lista_receitas}
    return render(request, 'receitas/buscar.html', dados)


def cria_receita(request):
    if request.method == 'POST':
        nome_receita = request.POST['nome_receita']
        ingredientes = request.POST['ingredientes']
        modo_preparo = request.POST['modo_preparo']
        tempo_preparo = request.POST['tempo_preparo']
        rendimento = request.POST['rendimento']
        categoria = request.POST['categoria']
        foto_receita = request.FILES['foto_receita']
        # requisição passando o id do autor para user
        user = get_object_or_404(User, pk=request.user.id)
        receita = Receita.objects.create(autor=user,
                                         nome_receita=nome_receita,
                                         ingredientes=ingredientes,
                                         modo_de_preparo=modo_preparo,
                                         tempo_de_preparo=tempo_preparo,
                                         rendimento=rendimento,
                                         categoria=categoria,
                                         foto_receita=foto_receita)
        # salvando a receita no banco de dados
        receita.save()
        return redirect('dashboard')
    else:
        return render(request, 'receitas/cria_receita.html')


def deleta_receita(request, receita_id):
    # recebendo o id do objeto receita
    receita = get_object_or_404(Receita, pk=receita_id)
    receita.delete()
    return redirect('dashboard')


def edita_receita(request, receita_id):
    # recebendo o id do objeto receita
    receita = get_object_or_404(Receita, pk=receita_id)
    receita_a_editar = {'receita': receita}
    return render(request, 'receitas/edita_receita.html', receita_a_editar)


def atualiza_receita(request):
    if request.method == 'POST':
        receita_id = request.POST['receita_id']
        # buscando o id da receita
        r = Receita.objects.get(pk=receita_id)
        r.nome_receita = request.POST['nome_receita']
        r.ingredientes = request.POST['ingredientes']
        r.modo_de_preparo = request.POST['modo_de_preparo']
        r.tempo_de_preparo = request.POST['tempo_de_preparo']
        r.rendimento = request.POST['rendimento']
        r.categoria = request.POST['categoria']
        if 'foto_receita' in request.FILES:
            r.foto_receita = request.FILES['foto_receita']
        r.save()
        return redirect('dashboard')
