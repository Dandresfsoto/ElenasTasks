import factory
from django.contrib.auth.models import User
from tasks.models import Tag, Task
from factory.fuzzy import FuzzyText, FuzzyChoice
from tasks.constants import (
    HIGHEST_PRIORITY_TASK,
    HIGH_PRIORITY_TASK,
    MEDIUM_PRIORITY_TASK,
    LOW_PRIORITY_TASK,
    LOWEST_PRIORITY_TASK
)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'user%d' % n)
    email = factory.LazyAttribute(lambda obj: '%s@elenas.co' % obj.username)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.Faker('name')


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    name = factory.Faker('name')
    description = FuzzyText(length=200)
    priority = FuzzyChoice(
        choices=[
            HIGHEST_PRIORITY_TASK,
            HIGH_PRIORITY_TASK,
            MEDIUM_PRIORITY_TASK,
            LOW_PRIORITY_TASK,
            LOWEST_PRIORITY_TASK
        ]
    )
    is_completed = FuzzyChoice(choices=[True, False])
