from rest_framework import generics
from rankingsApp.api.serializers import *
from rankingsApp.models import *
from django_filters.rest_framework import DjangoFilterBackend

class PlayerListView(generics.ListAPIView):
    queryset = PlayerModel.objects.all().order_by('Position', '-Rating', 'Name')
    serializer_class = PlayerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['Name', 'Rating', 'Team', 'Position']

class MatchupListView(generics.ListAPIView):
    queryset = MatchupModel.objects.all()
    serializer_class = MatchupSerializer