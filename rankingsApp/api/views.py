from rest_framework import generics
from rankingsApp.api.serializers import *
from rankingsApp.models import *


class PlayerListView(generics.ListAPIView):
    queryset = PlayerModel.objects.all().order_by('Position', '-Rating', 'Name')
    serializer_class = PlayerSerializer

class MatchupListView(generics.ListAPIView):
    queryset = MatchupModel.objects.all()
    serializer_class = MatchupSerializer