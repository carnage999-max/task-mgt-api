from .models import Task
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model
import logging
from faker import Faker
from random import choice
from datetime import timedelta
from django.utils import timezone
import pytz
import json
from django.forms.models import model_to_dict


User = get_user_model()
class TaskAPITest(APITestCase):
    fake = Faker()
    fake_task_name = fake.catch_phrase()
    fake_task_description = fake.paragraph(nb_sentences=3)
    fake_task_priority = choice(['low', 'high', 'urgent'])
    future_datetime = timezone.now() + timedelta(minutes=1)
    fake_task_deadline = fake.future_datetime(end_date=future_datetime, tzinfo=pytz.UTC)
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="cod3.culture@gmail.com", password="123ezekiel")
        self.task = Task.objects.create(
            user=self.user, name=self.fake_task_name, description=self.fake_task_description,
            priority=self.fake_task_priority, deadline=self.fake_task_deadline
        )
        self.task.save()
        login_response = self.client.post('/api/v1/users/login/', data={'email': "cod3.culture@gmail.com", "password": "123ezekiel"}, format='json').json()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login_response['access_token']}")
        
    def test_create_task(self):
        data_ = {
            "name": "Test Task", "description": "Task Description",
            "deadline": self.fake_task_deadline, "priority": self.fake_task_priority,
        }
        print("Testing Task Creation...")
        response = self.client.post('/api/v1/task/tasks/', data=data_, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_get_tasks(self):
        print("Testing Tasks List")
        response = self.client.get('/api/v1/task/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_task_by_id(self):
        print("Testing Task retrieval")
        response = self.client.get(f'/api/v1/task/tasks/{self.task.id}/')
        self.assertEqual(response.json()['name'], self.task.name)
        
    def test_task_delete(self):
        print("Testing Task deletion")
        response = self.client.delete(f"/api/v1/task/tasks/{self.task.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        
    def test_mark_task_complete(self):
        print("Testing Marking Tasks Complete")
        response = self.client.patch(f"/api/v1/task/tasks/{self.task.id}/mark_complete/")
        self.assertEqual(response.json()['status'], 'completed')
