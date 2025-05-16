from django.core.signals import request_finished
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.timezone import is_aware, make_aware
from datetime import datetime
from .models import Task
from .task import mark_as_due_and_notify
from django.db import transaction
import calendar
import pytz
import logging

utc = pytz.UTC

@receiver(post_save, sender=Task)
def schedule_task_deadlines(sender, instance, created, **kwargs):
    # seconds = calendar.timegm(time.utctimetuple()) - calendar.timegm((datetime.now()).utctimetuple())
    # print(f"{seconds} left")
    if created:
        eta = instance.deadline
        print(f"Deadline: {eta}")
        if is_aware(eta):
            eta = eta.astimezone(utc)
        mark_as_due_and_notify.apply_async(args=(instance.id,), eta=eta)