from rest_framework import serializers
from rankingsApp.models import Player, Matchup

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'Name', 'Rating', 'Team', 'Position', 'Age', 'Birthdate', 'Draftyear')
        extra_kwargs = {
            "id": {
                "read_only": False,
                "required": False,
            },
        }


class MatchupSerializer(serializers.ModelSerializer):
    PlayerOne = PlayerSerializer(many=False)
    PlayerTwo = PlayerSerializer(many=False)
    Winner = PlayerSerializer(many=False, required=False)
    class Meta:
        model = Matchup
        fields = ('PlayerOne', 'PlayerTwo', 'Winner')

    def create(self, validated_data):
        PlayerOne = Player.objects.get(id=validated_data.pop('PlayerOne')['id'])
        PlayerTwo = Player.objects.get(id=validated_data.pop('PlayerTwo')['id'])
        Winner = Player.objects.get(id=validated_data.pop('Winner')['id'])
        MatchUp = Matchup.objects.create(PlayerOne=PlayerOne, PlayerTwo=PlayerTwo, Winner=Winner)
        return MatchUp
