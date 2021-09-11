from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from rankingsApp.api.views import (
    PlayersView,
    MatchupsView,
    PlayersList,
    MatchupsList,
    RatingsList
)

app_name = 'rankingsApp'

urlpatterns = [
    path('ratings/', RatingsList.as_view(), name='ratingsList'),

    path('players/<int:pk>/', PlayersView.as_view(), name='playersView'),
    path('players/', PlayersList.as_view(), name='playersList'),

    path('matchups/<int:pk>/', MatchupsView.as_view(), name='matchupsView'),
    path('matchups/', MatchupsList.as_view(), name='matchupsList')
]

#urlpatterns = format_suffix_patterns(urlpatterns)