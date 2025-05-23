from django.db import models
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    # RepeatChoices = (
    #     ('daily', 'Daily'), ('monthly', 'Monthly'),
    #     ('yearly', 'Yearly'), ('never', 'Never')
    # )
    TASK_STATUS = (
        ('completed', 'Completed'), ('in_progress', 'In Progress'),
        ('not_started', 'Not Started'), ('on_hold', 'On Hold')
    )
    TASK_PRIORITY = (
        ('low', 'Low'), ('medium', 'Medium'),
        ('high', 'High'), ('urgent', 'Urgent')
    )
    user = models.ForeignKey('users.CustomUser', related_name='user_tasks', on_delete=models.CASCADE)
    name = models.CharField(_("task name"), max_length=50)
    description = models.TextField(blank=True, null=True)
    # repeat = models.CharField(_("repeat task"), max_length=10, choices=RepeatChoices)
    deadline = models.DateTimeField(_("task deadline"), blank=True, null=True)
    status = models.CharField(_("task status"), default='not_started', choices=TASK_STATUS, max_length=20)
    priority = models.CharField(_("task priority"), choices=TASK_PRIORITY, max_length=20, default='low')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))
    
    def __str__(self) -> str:
        return self.name
    
