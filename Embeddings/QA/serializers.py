from rest_framework import serializers
from QA.models import Qa

class QaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qa
        fields = ['question','created','answer']


