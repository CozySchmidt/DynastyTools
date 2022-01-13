from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rankingsApp.api.views.MatchupsView import MatchupsView, MatchupsList
from rankingsApp.api.views.PlayersView import PlayersList, PlayersView
from rankingsApp.api.views.UsersView import UsersList
from rankingsApp.api.views.RankingsView import RankingsList

app_name = 'rankingsApp'

urlpatterns = [
    path('users/', UsersList.as_view(), name='usersList'),
    path('rankings/', RankingsList.as_view(), name='rankingsList'),
    path('players/<int:pk>/', PlayersView.as_view(), name='playersView'),
    path('players/', PlayersList.as_view(), name='playersList'),
    path('matchups/<int:pk>/', MatchupsView.as_view(), name='matchupsView'),
    path('matchups/', MatchupsList.as_view(), name='matchupsList')
]
