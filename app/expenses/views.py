from django.forms import fields
from sources.models import Source
from rest_framework import viewsets
from .models import ExpensesGroup, Expense
from .serializers import ExpensesGroupSerializer, ExpenseSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthor
from rest_framework.exceptions import ValidationError
import django_filters

class ExpensesGroupViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthor, IsAuthenticated, )
    serializer_class = ExpensesGroupSerializer

    def get_queryset(self):
        user = self.request.user
        return ExpensesGroup.objects.filter(user_id=user)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user_id=self.request.user)


class ExpenseFilterSet(django_filters.FilterSet):
    date_start = django_filters.DateFilter(field_name="expense_date", lookup_expr="gte")
    date_end = django_filters.DateFilter(field_name="expense_date", lookup_expr="lte")
    
    class Meta:
        model = Expense
        fields = [
            'expense_name',
            'expense_value',
            'expense_date',
            'expense_group',
            'expense_source',
        ]

class ExpenseViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthor, IsAuthenticated, )
    serializer_class = ExpenseSerializer
    filterset_class = ExpenseFilterSet

    def get_queryset(self):
        user = self.request.user
        return Expense.objects.filter(user_id=user)

    def perform_create(self, serializer):
        if not self.expenseGroupExistsForUser(serializer):
            raise ValidationError(detail='This expense group is not defined in your account')
        elif not self.sourceExistsForUser(serializer):
            raise ValidationError(detail='This source is not defined in your account')
        else:
            serializer.save(user_id=self.request.user)


    def expenseGroupExistsForUser(self, serializer):
        user = self.request.user
        queryset = ExpensesGroup.objects.filter(user_id=user)
        name_list = [entry.expgroup_name for entry in queryset]
        expense_group = serializer.validated_data.get('expense_group')
        return str(expense_group) in name_list
    
    def sourceExistsForUser(self, serializer):
        user = self.request.user
        queryset = Source.objects.filter(user_id=user)
        name_list = [entry.source_name for entry in queryset]
        source_group = serializer.validated_data.get('expense_source')
        return str(source_group) in name_list

    def perform_update(self, serializer):
        serializer.save(user_id=self.request.user)