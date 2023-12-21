from django.contrib import admin
from .models import Team,PlayerProfile,Game,UserLogs,PlayerGame
# Register your models here.

admin.site.register(Team)
admin.site.register(PlayerProfile)
admin.site.register(Game)
admin.site.register(UserLogs)
admin.site.register(PlayerGame)