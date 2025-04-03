from rest_framework import viewsets
from .models import transacao
from .serializers import TransacaoSerializer
from django.shortcuts import render
import pandas as pd
from django.http import HttpResponse
from reportlab.pdfgen import canvas

class TransacaoViewSet(viewsets.ModelViewSet):
    queryset = transacao.objects.all()
    serializer_class = TransacaoSerializer

def dashboard(request):
    return render(request, 'dashboard.html')

def exportar_excel(request):
    transacoes = transacao.objects.all().values()
    df = pdf.DataFrame(transacoes)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="relatorio.xlsx"'
    df.to_excel(response,index=False)
    return response

def exportar_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio.pdf"'
    pdf = canvas.Canvas(response)
    pdf.drawString(100, 800, "Relatório Financeiro")
    pdf.save()
    return response