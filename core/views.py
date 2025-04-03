from rest_framework import viewsets
from .models import transacao
from .serializers import TransacaoSerializer
from django.shortcuts import render
import pandas as pd
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

class TransacaoViewSet(viewsets.ModelViewSet):
    """
    API Viewset para gerenciar transações financeiras.
    Fornece operações CRUD completas através da API REST.
    """
    queryset = transacao.objects.all()
    serializer_class = TransacaoSerializer
    
    # Removido o método get_queryset que causava o erro

def dashboard(request):
    """
    Renderiza a página do dashboard que mostra gráficos financeiros.
    """
    return render(request, 'dashboard.html')

def exportar_excel(request):
    """
    Exporta todas as transações para um arquivo Excel.
    
    Inclui detalhes como tipo de transação, descrição, valor e data.
    O arquivo é oferecido como um download para o usuário.
    """
    # Obtém todas as transações (sem filtro por usuário)
    transacoes = transacao.objects.all().values()
    
    # Converte os dados para um DataFrame do pandas
    df = pd.DataFrame(transacoes)
    
    # Substitui os códigos R/D pelos valores completos (se o dataframe não estiver vazio)
    if len(df) > 0 and 'tipo' in df.columns:
        df['tipo'] = df['tipo'].replace({'R': 'Receita', 'D': 'Despesa'})
    
    # Configura a resposta HTTP como um arquivo Excel
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename="relatorio_financeiro.xlsx"'
    
    # Salva o DataFrame para o response
    df.to_excel(response, index=False)
    return response

def exportar_pdf(request):
    """
    Exporta transações para um arquivo PDF formatado.
    
    Cria um relatório PDF com uma tabela de transações e um cabeçalho.
    O arquivo é oferecido como um download para o usuário.
    """
    # Configura a resposta HTTP como um arquivo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_financeiro.pdf"'
    
    # Cria o objeto Canvas para desenhar o PDF
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    
    # Adiciona um título ao PDF
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 50, "Relatório Financeiro")
    
    # Obtém as transações
    transacoes = transacao.objects.all()
    
    # Posição inicial para listar as transações
    y_position = height - 100
    
    # Adiciona cabeçalhos
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y_position, "Tipo")
    p.drawString(150, y_position, "Descrição")
    p.drawString(350, y_position, "Valor")
    p.drawString(450, y_position, "Data")
    y_position -= 20
    
    # Desenha uma linha separadora
    p.line(50, y_position - 5, 550, y_position - 5)
    y_position -= 15
    
    # Adiciona as transações
    p.setFont("Helvetica", 10)
    for t in transacoes:
        tipo_texto = 'Receita' if t.tipo == 'R' else 'Despesa'
        
        p.drawString(50, y_position, tipo_texto)
        p.drawString(150, y_position, t.descricao)
        p.drawString(350, y_position, f"R$ {t.valor:.2f}")
        p.drawString(450, y_position, t.data.strftime('%d/%m/%Y'))
        
        y_position -= 20
        
        # Se chegou ao final da página, cria uma nova
        if y_position < 50:
            p.showPage()
            y_position = height - 50
    
    # Finaliza o PDF
    p.showPage()
    p.save()
    
    return response