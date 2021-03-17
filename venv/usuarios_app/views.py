from django.shortcuts import render, get_object_or_404
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
