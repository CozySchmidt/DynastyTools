from rankingsApp.api.serializers import *
from rankingsApp.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class UsersList(APIView):
    """
    Create new user
    """
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            rankings = Ranking.objects.filter(User__Username="Global")
            for ranking in rankings:
                ranking.pk = None
                ranking.User = user.id
            rankings.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

