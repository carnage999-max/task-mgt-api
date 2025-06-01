from .models import Task
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timezone


def is_90_percent_due(task):
    if not task.deadline:
        return False
    total_duration = (task.deadline - task.created_at).total_seconds()
    if total_duration <= 0:
        return False
    elapsed_duration = (datetime.now(timezone.utc) - task.created_at).total_seconds()
    return elapsed_duration >= 0.9 * total_duration


def send_reminder_mail(task_id):
    task = Task.objects.get(id=task_id)
    try:
        send_mail(
        subject = "YOUR TASK IS Almost DUE!",
        message = f"Your task - {task.name} is Almost due.\n Deadline is {task.deadline}",
        from_email = settings.DEFAULT_FROM_EMAIL,
        recipient_list = [task.user.email,],
        fail_silently=False
    )
    except Exception as e:
        print(e)