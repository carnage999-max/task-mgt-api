from .models import Task
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .factories import UserFactory, TaskFactory
from rest_framework_simplejwt.tokens import RefreshToken
from random import choice
from django.utils import timezone
from datetime import timedelta


User = get_user_model()
class BaseTaskTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.task = TaskFactory.create(user=self.user)
        token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")
        
class TaskCreateTests(BaseTaskTestCase):
    def test_create_task(self):
        data_ = {
            "name": "Test Task", "description": "Task Description",
            "deadline": timezone.now()+timedelta(minutes=1), "priority": choice(['low', 'high', 'urgent']),
        }
        print("Testing Task Creation...")
        response = self.client.post(reverse('task-list'), data=data_, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_unauthenticated_task_creation(self):
        data_ = {
            "name": "Test Task", "description": "Task Description",
            "deadline": timezone.now()+timedelta(minutes=1), "priority": choice(['low', 'high', 'urgent']),
        }
        self.client.credentials()
        response = self.client.post(reverse('task-list'), data=data_, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_task_creation_with_missing_required_field(self):
        data_ = {
            "description": "Task Description",
            "deadline": timezone.now()+timedelta(minutes=1), "priority": choice(['low', 'high', 'urgent']),
        }
        response = self.client.post(reverse('task-list'), data=data_, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_task_creation_with_past_deadline(self):
        data_ = {
            "description": "Task Description",
            "deadline": timezone.now()-timedelta(minutes=5), "priority": choice(['low', 'high', 'urgent']),
        }
        response = self.client.post(reverse('task-list'), data=data_)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
class TaskGetTest(BaseTaskTestCase):
    def test_unauthenticated_task_get(self):
        self.client.credentials()
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_tasks(self):
        print("Testing Tasks List")
        TaskFactory.create_batch(5, user=self.user)
        TaskFactory.create_batch(3)
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_task_by_id(self):
        print("Testing Task retrieval")
        response = self.client.get(reverse('task-detail', kwargs={"pk":self.task.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], self.task.name)
        
    def test_get_task_by_incorrect_task_id(self):
        response = self.client.get(reverse('task-detail', kwargs={"pk":9999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
class TaskDeleteTests(BaseTaskTestCase):
    def test_unauthenticated_task_delete(self):
        self.client.credentials()
        response = self.client.delete(reverse('task-detail', kwargs={"pk":self.task.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
        
    def test_task_delete(self):
        print("Testing Task deletion")
        response = self.client.delete(reverse('task-detail', kwargs={"pk":self.task.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
class TaskUpdateTests(BaseTaskTestCase):        
    def test_mark_task_complete(self):
        print("Testing Marking Tasks Complete")
        response = self.client.patch(reverse('task-mark-complete', kwargs={'pk': self.task.id}))
        self.assertEqual(response.json()['status'], 'completed')
        
    def test_task_partial_update(self):
        data_ = {"name": "A new hope"}
        response = self.client.patch(reverse('task-detail', kwargs={"pk": self.task.id}), data=data_)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "A new hope")
        
    def test_updating_a_completed_task(self):
        self.task.status = "completed"
        data = {"deadline": self.task.deadline + timedelta(days=7)}
        response = self.client.put(reverse('task-detail', kwargs={'pk': self.task.id}), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        
class TaskCountTests(BaseTaskTestCase):
    def test_database_count_increase_on_task_create(self):
        count_before = Task.objects.count()
        TaskFactory.create_batch(1, user=self.user)
        self.assertEqual(Task.objects.count(), count_before+1)
        
    def test_database_count_decrease_on_task_delete(self):
        count_before = Task.objects.count()
        self.client.delete(reverse("task-detail", kwargs={"pk":self.task.id}))
        self.assertEqual(Task.objects.count(), count_before-1)
    
