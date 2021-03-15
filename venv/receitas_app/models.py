from django.db import models
from datetime import datetime
from pessoas_app.models import Pessoa

class Receita(models.Model):
    autor               = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    nome_receita        = models.CharField(max_length=200)
    ingredientes        = models.TextField()
    modo_de_preparo     = models.TextField()
    tempo_de_preparo    = models.IntegerField()
    rendimento          = models.CharField(max_length=100)
    categoria           = models.CharField(max_length=100)
    data_receita        = models.DateField(default=datetime.now, blank=True)
