from django.db import models
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    RepeatChoices = (
        ('daily', 'Daily'), ('monthly', 'Monthly'),
        ('yearly', 'Yearly'), ('never', 'Never')
    )
    
    name = models.CharField(_("task name"), max_length=50)
    description = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    repeat = models.CharField(_("repeat task"), max_length=10, choices=RepeatChoices)
    
    def __str__(self) -> str:
        return self.name
    
