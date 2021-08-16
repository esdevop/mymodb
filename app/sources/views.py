from rest_framework import viewsets
from .models import Source
from .serializers import SourceSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthor

class SourceViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthor, IsAuthenticated, )
    serializer_class = SourceSerializer

    def get_queryset(self):
        user = self.request.user
        return Source.objects.filter(user_id=user)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user_id=self.request.user)
