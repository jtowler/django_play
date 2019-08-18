from django.conf import settings
from django.db import models
from django.utils import timezone


class Exercise(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    sets = models.IntegerField(default=1)
    reps = models.IntegerField(default=1)
    weight = models.FloatField(default=0.0)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name}: {self.sets}x{self.reps} at {self.weight}kg"
