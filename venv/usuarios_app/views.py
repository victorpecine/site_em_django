from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from receitas_app.models import Receita


def cadastro(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']
        if campo_vazio(nome):
            messages.error(request, 'O nome não pode ficar em branco')
            return redirect('cadastro')
        if campo_vazio(email):
            messages.error(request, 'O e-mail não pode ficar em branco')
            return redirect('cadastro')
        if senhas_nao_iguais(senha, senha2):
            messages.error(request, 'As senhas digitadas não são iguais')
            return redirect('cadastro')
        # verificando pelo e-mail se o usuário já está no banco de dados
        if User.objects.filter(email=email).exists():
            messages.error(request, 'E-mail já cadastrado')
            return redirect('cadastro')
        if User.objects.filter(username=nome).exists():
            messages.error(request, 'Nome já cadastrado')
            return redirect('cadastro')
        user = User.objects.create_user(username=nome, email=email, password=senha)
        user.save()
        messages.success(request, 'Usuário cadastrado com sucesso')
        return redirect('login')
    else:
        return render(request, 'usuarios/cadastro.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        if campo_vazio(email) or campo_vazio(senha):
            messages.error(request, 'Os campos devem ser preenchidos')
            return redirect('login')
        if User.objects.filter(email=email).exists():
            # filtrando o username a partir do e-mail
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)
            # fazendo a autenticação do usuário e senha
            if user is not None:
                auth.login(request, user)
                print('Login realizado com sucesso')
        return redirect('dashboard')
    return render(request, 'usuarios/login.html')


def logout(request):
    auth.logout(request)
    return redirect('index')


def dashboard(request):
    if request.user.is_authenticated:
        id = request.user.id
        # mostrando apenas as receitas do autor(user) filtradas pelo id
        receitas = Receita.objects.order_by('-data_receita').filter(autor=id)
        # passando as informações(dados) para o template
        dados = {'receitas': receitas}
        return render(request, 'usuarios/dashboard.html', dados)
    else:
        return redirect('index')


def campo_vazio(campo):
    return not campo.strip()


def senhas_nao_iguais(senha, senha2):
    return senha != senha2


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
        return render(request, 'usuarios/cria_receita.html')


def deleta_receita(request, receita_id):
    # recebendo o id do objeto receita
    receita = get_object_or_404(Receita, pk=receita_id)
    receita.delete()
    return redirect('dashboard')


def edita_receita(request, receita_id):
    # recebendo o id do objeto receita
    receita = get_object_or_404(Receita, pk=receita_id)
    receita_a_editar = {'receita': receita}
    return render(request, 'usuarios/edita_receita.html', receita_a_editar)


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
