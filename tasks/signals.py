from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.timezone import is_aware
from .models import Task
from .task import mark_as_due_and_notify, send_reminder_email
import pytz

utc = pytz.UTC

@receiver(post_save, sender=Task)
def schedule_task_deadlines(sender, instance, created, **kwargs):
    if created:
        eta = instance.deadline
        if is_aware(eta):
            eta = eta.astimezone(utc)
        # Schedule the reminder task at 90% of the way to deadline
        total_time = (eta - instance.created_at).total_seconds()
        print(f"Total time - {total_time}")
        reminder_time = int(total_time * 0.75)
        print(f"Reminder is in - {reminder_time} seconds")
        if reminder_time > 0:
            send_reminder_email.apply_async((instance.id,), countdown=reminder_time)
        mark_as_due_and_notify.apply_async(args=(instance.id,), eta=eta)