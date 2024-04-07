from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role_choices = (
        ('1', 'Superuser'),
        ('2', 'Member'),
        ('3', 'User')
    )
    role = models.CharField(max_length=50, choices=role_choices ,default='3')
    phone_number = models.CharField(max_length=50, blank=True, null=True, unique=True)
    points = models.IntegerField(default=0)
    
    def __str__(self):
        return self.user.username
    
class StartEvent(models.Model):
    start_time = models.DateTimeField()
    
    def __str__(self):
        return str(self.start_time)

