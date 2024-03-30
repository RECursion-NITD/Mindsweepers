from django.db import models
from website.models import Profile


class Game(models.Model):
    ques_string = models.CharField(max_length=100, null=True)
    game_user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    moves = models.IntegerField()
    game_string_arr = models.JSONField(default=dict)

    def __str__(self):
        return self.game_user.user.username
