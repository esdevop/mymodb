from rest_framework import serializers
from .models import Income, IncomesGroup


class IncomesGroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'incgroup_name',)
        model = IncomesGroup
        

class IncomeSerializer(serializers.ModelSerializer):
    

    class Meta:
        fields = (
            'id', 
            'income_name',
            'income_value',
            'income_date',
            'income_group',
            'income_source',
        )
        model = Income 