from rankingsApp.api.serializers import *
from rankingsApp.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

Valid_Positions = ['QB', 'RB', 'WR', 'TE']

class PlayersList(APIView):
    """
    List all Players
    """
    def get(self, request):
        position = request.GET.get('position')
        players = Player.objects.all().order_by('Name')
        if position in Valid_Positions:
            players = players.filter(Position=position)
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)

    """
    Create new player
    """
    def post(self, request):
        serializer = PlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlayersView(APIView):
    """
    internal method to get player
    """
    def get_object(self, pk):
        try:
            return Player.objects.get(id=pk)
        except Player.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        pid = self.kwargs['pk']
        players = self.get_object(pk=pid)
        serializer = PlayerSerializer(players, many=False)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        pid = self.kwargs['pk']
        player = self.get_object(pk=pid)
        serializer = PlayerSerializer(player, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        pid = self.kwargs['pk']
        player = self.get_object(pk=pid)
        serializer = PlayerSerializer(player, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pid = self.kwargs['pk']
        player = self.get_object(pk=pid)
        player.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
