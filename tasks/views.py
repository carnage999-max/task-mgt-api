from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from rest_framework import status
from rest_framework.decorators import action
import datetime
import pytz
from django.utils import timezone

utc = pytz.UTC
class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        deadline = serializer.validated_data['deadline']
        print(f"Deadline: {deadline}")
        print(f"now: {datetime.datetime.now()}")
        if deadline and deadline <= timezone.now():
            return Response({
                "error": "deadline cannot be a date/time that has passed"
            })
        deadline = deadline.astimezone(pytz.UTC)
        serializer.validated_data['deadline'] = deadline
        
        print(f"Deadline UTC: {deadline}")
        print(f"Submitted Deadline UTC: {serializer.validated_data['deadline']}")
        serializer.save()
        task = Task.objects.get(id=serializer.data.get('id'))
        task.status = "in_progress"
        task.save()
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def completed_tasks(self, request):
        tasks = self.get_queryset().filter(status='completed')
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
