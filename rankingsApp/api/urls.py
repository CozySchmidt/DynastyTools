from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from rankingsApp.api.views import (
    PlayersView,
    MatchupsView,
    PlayersList
)

app_name = 'rankingsApp'

urlpatterns = [
    path('players/<int:playerid>/', PlayersView.as_view()),
    path('players/', PlayersList.as_view()),
    path('matchups/', MatchupsView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)