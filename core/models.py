from django.db import models
from django.contrib.auth.models import User

class transacao(models.Model):
    TIPOS = (
        ('R', 'Receita'),
        ('D', 'Despesa')
    )
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=1, choices=TIPOS)
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()

    def __str__(self):
        return f"{self.descricao} - {self.valor}"