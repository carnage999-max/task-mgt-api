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
        print(task)
        logging.info(f"Now: {timezone.now()}")
        logging.info(f"deadline: {task.deadline}")
        if task.deadline <= timezone.now()+datetime.timedelta(hours=1):
            task.status = 'completed'
            task.save()
            logging.info(f"Task is due: sending email for task '{task.name}' to {task.user.email}")
            add.delay(3,8)
    except Task.DoesNotExist:
        return {"error": "does not exist"}
    
@shared_task
def send_due_mail(task_id):
    task = Task.objects.get(id=task_id)
    try:
        send_mail(
        subject = "TASK DUE!",
        message = f"Your task - {task.name} is now due.",
        from_email = 'jamesezekiel039@gmail.com',
        recipient_list = [task.user.email,],
        fail_silently=False
    )
    except Task.DoesNotExist:
        pass
    
    
@shared_task
def add(x,y):
    return x+y