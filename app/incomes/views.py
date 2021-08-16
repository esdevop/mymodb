#from sources.models import Source
from rest_framework import viewsets
from .models import Income, IncomesGroup
from .serializers import IncomeSerializer, IncomesGroupSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthor
from rest_framework.exceptions import ValidationError
from sources.models import Source
import django_filters

class IncomesGroupViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthor, IsAuthenticated, )
    serializer_class = IncomesGroupSerializer

    def get_queryset(self):
        user = self.request.user
        return IncomesGroup.objects.filter(user_id=user)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user_id=self.request.user)



class IncnomeFilterSet(django_filters.FilterSet):
    date_start = django_filters.DateFilter(field_name="income_date", lookup_expr="gte")
    date_end = django_filters.DateFilter(field_name="income_date", lookup_expr="lte")
    
    class Meta:
        model = Income 
        fields = [
            'income_name',
            'income_value',
            'income_date',
            'income_group',
            'income_source',
        ]


class IncomeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthor, IsAuthenticated, )
    serializer_class = IncomeSerializer 
    filterset_class = IncnomeFilterSet

    def get_queryset(self):
        user = self.request.user
        return Income.objects.filter(user_id=user)

    def perform_create(self, serializer):
        if not self.incomeGroupExistsForUser(serializer):
            raise ValidationError(detail='This income group is not defined in your account')
        elif not self.sourceExistsForUser(serializer):
            raise ValidationError(detail='This source is not defined in your account')
        else:
            serializer.save(user_id=self.request.user)

    def incomeGroupExistsForUser(self, serializer):
        user = self.request.user
        queryset = IncomesGroup.objects.filter(user_id=user)
        name_list = [entry.incgroup_name for entry in queryset]
        income_group = serializer.validated_data.get('income_group')
        return str(income_group) in name_list
    
    def sourceExistsForUser(self, serializer):
        user = self.request.user
        queryset = Source.objects.filter(user_id=user)
        name_list = [entry.source_name for entry in queryset]
        source_group = serializer.validated_data.get('income_source')
        return str(source_group) in name_list

    def perform_update(self, serializer):
        serializer.save(user_id=self.request.user)