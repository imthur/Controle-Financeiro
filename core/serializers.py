from rest_framework import serializers
from .models import transacao

class TransacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = transacao
        fields = '__all__'