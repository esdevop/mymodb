from rest_framework import serializers
from .models import Expense, ExpensesGroup


class ExpensesGroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'expgroup_name',)
        model = ExpensesGroup


class ExpenseSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'id', 
            'expense_name',
            'expense_value',
            'expense_date',
            'expense_group',
            'expense_source',
        )
        model = Expense