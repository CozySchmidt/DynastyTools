from django.contrib import admin
from .models import Player, Matchup, User, Rating

# Register your models here.
admin.site.register(Player)
admin.site.register(Matchup)
admin.site.register(User)
admin.site.register(Rating)