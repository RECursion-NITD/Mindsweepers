from django.db import models
from website.models import Profile


class GraphGame(models.Model):
    game_user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tree_structure = models.JSONField()
    moves = models.IntegerField(default=0)
    last_reset_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"GraphGame for {self.game_user.user.username}"
