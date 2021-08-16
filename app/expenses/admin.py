from django.contrib import admin
from .models import Expense, ExpensesGroup


admin.site.register(ExpensesGroup)
admin.site.register(Expense)
