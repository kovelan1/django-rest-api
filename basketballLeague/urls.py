"""
URL configuration for basketballLeague project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('games/',view.game_list),
    path('scoreboard/',view.get_score_board),
    path('team/coach/', view.get_team_by_coach),
    path('player/<int:player_id>',view.get_player_info),
    path('player/heighscore', view.get_90_percentile_players),
    path('teams/', view.get_teams),
    path('signup',view.signup),
    path('login',view.login),





]
