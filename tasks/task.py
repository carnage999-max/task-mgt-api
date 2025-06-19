from celery import shared_task
import datetime
from .models import Task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import logging
import requests
from decouple import config
from django.contrib.auth import get_user_model


User = get_user_model()

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
def send_reminder_email(task_id):
    try:
        task = Task.objects.get(id=task_id)
        if not task.deadline:
            return  # Skip tasks with no deadline
        # time_elapsed = (timezone.now() - task.created_at).total_seconds()
        # total_time = (task.deadline - task.created_at).total_seconds()
        # if time_elapsed / total_time >= 0.9 and task.status != 'completed':
        send_mail(
            subject=f"Reminder: Task '{task.name}' is almost due",
            message=f"Your task '{task.name}' is nearing its deadline.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[task.user.email],
            fail_silently=False
        )
    except Exception as e:
        logging.error(e)
        

@shared_task
def send_telegram_notification(task_id):
    try:
        task = Task.objects.get(id=task_id)
        user = User.objects.get(id=task.user.id)
        chat_id = user.telegram_chat_id

        if not chat_id:
            print(f"No Telegram chat ID for user {user.username}")
            return

        bot_token = config("TELEGRAM_BOT_TOKEN")
        telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        message = f"Reminder: Task '{task.name}' deadline reached on {task.deadline}!"

        response = requests.post(telegram_url, data={
            "chat_id": chat_id,
            "text": message
        })

        if response.status_code == 200:
            print(f"Telegram notification sent to {user.username}")
        else:
            print(f"Failed to send Telegram notification: {response.text}")
            raise Exception("Telegram API error")

    except (User.DoesNotExist, user.DoesNotExist):
        print(f"User or profile not found for ID {task.user.id}")
    except Exception as e:
        print(f"Error sending Telegram notification: {str(e)}")
