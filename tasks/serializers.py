from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    class Meta:
        model = Task
        fields = [
            'id', 'user', 'name', 'description', 'deadline',
            'status', 'priority', 'created_at', 'updated_at', 'user_email'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'status']
        required_fields = ['name']

    def create(self, validated_data):
        user = self.context['request'].user
        return Task.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        instance.user = self.context['request'].user
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.deadline = validated_data.get('deadline', instance.deadline)
        instance.status = validated_data.get('status', instance.status)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.save()
        return instance