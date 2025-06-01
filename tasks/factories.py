import factory
from django.utils import timezone
from datetime import timedelta
from users.models import CustomUser
from tasks.models import Task


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    username = factory.Sequence(lambda n: f"user{n}")
    password = factory.PostGenerationMethodCall('set_password', 'testpass')


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    user = factory.SubFactory(UserFactory)
    name = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("paragraph")
    deadline = factory.LazyFunction(lambda: timezone.now() + timedelta(days=2))
    status = "not_started"
    priority = "low"
