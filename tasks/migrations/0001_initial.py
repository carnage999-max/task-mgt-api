# Generated by Django 5.2.1 on 2025-05-09 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='name', max_length=50, verbose_name='task name')),
                ('description', models.TextField(blank=True, null=True)),
                ('deadline', models.DateTimeField(blank=True, null=True, verbose_name='task deadline')),
                ('status', models.CharField(choices=[('completed', 'Completed'), ('in_progress', 'In Progress'), ('not_started', 'Not Started'), ('on_hold', 'On Hold')], default='not_started', max_length=20, verbose_name='task status')),
                ('priority', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('urgent', 'Urgent')], default='low', max_length=20, verbose_name='task priority')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
            ],
        ),
    ]
