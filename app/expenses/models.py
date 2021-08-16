from django.db import models
from django.contrib.auth.models import User
from sources.models import Source
from django.contrib.auth import get_user_model


class ExpensesGroup(models.Model):
    user_id = models.ForeignKey(get_user_model(), to_field='id', on_delete=models.CASCADE)
    expgroup_name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.expgroup_name


class Expense(models.Model):
    user_id = models.ForeignKey(get_user_model(), to_field='id', on_delete=models.CASCADE)
    expense_name = models.CharField(max_length=50)
    expense_value = models.DecimalField(max_digits=9, decimal_places=2)
    expense_date = models.DateField()
    expense_group = models.ForeignKey(ExpensesGroup, to_field='id', on_delete=models.CASCADE)
    expense_source = models.ForeignKey(Source, to_field='id', on_delete=models.CASCADE)

    def __str__(self):
        return self.expense_name
