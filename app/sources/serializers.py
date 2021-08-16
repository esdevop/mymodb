from rest_framework import serializers
from .models import Source


class SourceSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'source_name', 'source_value',)
        model = Source