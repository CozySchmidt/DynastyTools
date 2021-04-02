from django.conf.urls import url

from rankingsApp.api.views import (
    PlayerListView,
    MatchupListView
)

app_name = 'rankingsApp'

urlpatterns = [
    url(r'^players', PlayerListView.as_view()),
    url(r'^matchups', MatchupListView.as_view())
]