from celery import shared_task
import datetime
from .models import Task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import logging



@shared_task
def mark_as_due_and_notify(task_id):
    try:
        task = Task.objects.get(id=task_id)
        if task.deadline <= timezone.now():
            logging.info(f"Task is due: sending email for task '{task.name}' to {task.user.email}")
            send_due_mail.delay(task.id)
            task.status = 'completed'
            task.save()
    except Task.DoesNotExist:
        logging.error("Task does not exist")
    
@shared_task
def send_due_mail(task_id):
    task = Task.objects.get(id=task_id)
    try:
        send_mail(
        subject = "YOUR TASK IS DUE!",
        message = f"Your task - {task.name} is now due.",
        from_email = settings.DEFAULT_FROM_EMAIL,
        recipient_list = [task.user.email,],
        fail_silently=False
    )
    except Exception as e:
        logging.error(e)
        
@shared_task
def send_reminder_mail(task_id):
    task = Task.objects.get(id=task_id)
    