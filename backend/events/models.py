from django.db import models
from django.contrib.auth import get_user_model
from datetime import timedelta

User = get_user_model()

class Event(models.Model):
    REPEAT_CHOICES = [('NONE', 'None'), ('WEEKLY', 'Weekly')]
    name = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    repeat = models.CharField(max_length=10, choices=REPEAT_CHOICES, default='NONE')
    repeat_days = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(User, related_name='events', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def duration(self):
        ''' Calculate the duration based on start_time and end_time '''
        return self.end_time - self.start_time
