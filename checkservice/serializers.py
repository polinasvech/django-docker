from rest_framework import serializers
from .models import Printer, Check

class CheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = '__all__'
