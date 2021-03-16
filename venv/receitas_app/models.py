from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Receita(models.Model):
    autor               = models.ForeignKey(User, on_delete=models.CASCADE)
    nome_receita        = models.CharField(max_length=200)
    ingredientes        = models.TextField()
    modo_de_preparo     = models.TextField()
    tempo_de_preparo    = models.IntegerField()
    rendimento          = models.CharField(max_length=100)
    categoria           = models.CharField(max_length=100)
    data_receita        = models.DateField(default=datetime.now, blank=True)
    receita_publicada   = models.BooleanField(default=False)
    # imagens referenciadas pela data dia/mês/ano
    foto_receita        = models.ImageField(upload_to='fotos/%d/%m/%Y/', blank=True)

    def __str__(self):
        return self.nome_receita