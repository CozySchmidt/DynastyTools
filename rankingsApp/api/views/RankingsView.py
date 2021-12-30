from rankingsApp.api.serializers import *
from rankingsApp.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.urls import path

Valid_Positions = ['QB', 'RB', 'WR', 'TE']

"""
Get list of rankings by username.  Uses Global if username not found
"""
class RankingsList(APIView):
    def get(self, request):
        username = request.GET.get('username')
        username = username if username is not None else "Global"
        rankings = Ranking.objects.filter(User__Username=username)
        
        position = request.GET.get('position')
        if position in Valid_Positions:
            rankings = rankings.filter(Player__Position=position)
        
        rankings = rankings.order_by('-Rating', 'Player__Name')

        serializer = RankingSerializer(rankings, many=True)
        return Response(serializer.data)
