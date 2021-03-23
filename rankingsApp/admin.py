from django.contrib import admin
from .models import PlayerModel, MatchupModel

# Register your models here.
admin.site.register(PlayerModel)
admin.site.register(MatchupModel)