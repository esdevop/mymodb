from django.db import models
from sources.models import Source
from django.contrib.auth import get_user_model


class IncomesGroup(models.Model):
    user_id = models.ForeignKey(get_user_model(), to_field='id', on_delete=models.CASCADE)
    incgroup_name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.incgroup_name
class Income(models.Model):
    user_id = models.ForeignKey(get_user_model(), to_field='id', on_delete=models.CASCADE)
    income_name = models.CharField(max_length=50)
    income_value = models.DecimalField(max_digits=9, decimal_places=2)
    income_date = models.DateField()
    income_group = models.ForeignKey(IncomesGroup, to_field='id', on_delete=models.CASCADE)
    income_source = models.ForeignKey(Source, to_field='id', on_delete=models.CASCADE)

    def __str__(self):
        return self.income_name