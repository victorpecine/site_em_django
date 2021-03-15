from django.db import models

class Pessoa(models.Model):
    nome_pessoa = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.nome_pessoa