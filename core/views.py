from rest_framework import viewsets
from .models import transacao
from .serializers import TransacaoSerializer
from django.shortcuts import render

class TransacaoViewSet(viewsets.ModelViewSet):
    queryset = transacao.objects.all()
    serializer_class = TransacaoSerializer

def dashboard(request):
    return render(request, 'dashboard.html')