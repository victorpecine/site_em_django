from django.db import models
from datetime import datetime

class Receita(models.Model):
    nome_receita        = models.CharField(max_length=200)
    ingredientes        = models.TextField()
    mode_de_preparo     = models.TextField()
    tempo_de_preparo    = models.IntegerField()
    rendimento          = models.CharField(max_length=100)
    categoria           = models.CharField(max_length=100)
    data_receita        = models.DateField(defaut=datetime.now, blank=True)
    
