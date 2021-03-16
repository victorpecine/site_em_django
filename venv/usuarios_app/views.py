from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from receitas_app.models import Receita

def cadastro(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']
        if not nome.strip():
            print('O campo nome não pode ficar me branco')
            return redirect('cadastro')
        if not email.strip():
            print('O campo e-mail não pode ficar me branco')
            return redirect('cadastro')
        if senha != senha2:
            print('As senhas digitadas não são iguais')
            return redirect('cadastro')
        # verificando pelo e-mail se o usuário já está no banco de dados
        if User.objects.filter(email=email).exists():
            print('Usuário já cadastrado')
            return redirect('cadastro')
        user = User.objects.create_user(username=nome, email=email, password=senha)
        user.save()
        print('Usuário cadastrado com sucesso')
        print(nome, email, senha, senha2)
        return redirect('login')
    else:
        return render(request, 'usuarios/cadastro.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        if email == '' or senha == '':
            print('O e-mail e a senha não podem ficar vazios')
            return redirect('login')
        print(email, senha)
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
        # mostrando apenas as receitas do autor(user) filtradas pelo respectivo id
        receitas = Receita.objects.order_by('-data_receita').filter(autor=id)
        # passando as informações(dados) para o template
        dados = {'receitas': receitas}
        return render(request, 'usuarios/dashboard.html', dados)
    else:
        return redirect('index')

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
