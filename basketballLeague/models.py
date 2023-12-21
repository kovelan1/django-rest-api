from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

# Team model contains name and coach assigned
# Coach is mapped from user -> group
class Team(models.Model):
    name = models.CharField(max_length=100)
    coach = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name='team')

    class Meta:
        permissions = [
            ("view_own_team", "Can view own team"),
        ]

    def __str__(self):
        return self.name +' - '+self.coach.username

# PlayerProfile have the user as player , player's height and team the player belongs to
class PlayerProfile(models.Model):
    player = models.OneToOneField(User, on_delete=models.CASCADE)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name='players')

    def __str__(self):
        return self.team.name +' - '+self.player.username+' - '+str(self.height)

#game type enum
class GameType(models.TextChoices):
    LEAGUE_STAGE = "League Stage", "League Stage"
    QUARTER_FINAL = "Quarter-Final", "Quarter-Final"
    SEMI_FINAL = "Semi-Final", "Semi-Final"
    FINAL = "Final", "Final"

# Games is the two team participant and winner and the final score of the each
class Game(models.Model):
    date = models.DateTimeField()
    game_type = models.CharField(
        max_length=50,
        choices=GameType.choices,
        default=GameType.LEAGUE_STAGE
    )
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_games')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_games')
    team1_score = models.IntegerField()
    team2_score = models.IntegerField()
    winner = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)+'-'+self.game_type+'-'+str(self.date) +'- '+self.team1.name+' - '+self.team1.name+' - '+self.team2.name+'- '+self.winner.name+' - '+str(self.team1_score)+' - '+str(self.team2_score)

# define the relationship of player wih game
class PlayerGame(models.Model):
    game= models.ForeignKey(Game, on_delete=models.CASCADE, related_name='player_games')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player_games')
    score = models.IntegerField()

    def __str__(self):
        return str(self.game.id)+' - '+self.user.username+' - '+str(self.score)

# user status to manage the user logs
class UserLogs(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    login_count = models.IntegerField(default=0)
    total_time_spent = models.DurationField()
    is_loged_in = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username+' - '+str(self.login_count)+' - '+str(self.total_time_spent)+' - '+str(self.is_loged_in)+' - '+str(self.last_login)


