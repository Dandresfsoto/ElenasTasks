import factory
from factory.fuzzy import FuzzyText, FuzzyChoice

from tasks.constants import (
    HIGHEST_PRIORITY_TASK,
    HIGH_PRIORITY_TASK,
    MEDIUM_PRIORITY_TASK,
    LOW_PRIORITY_TASK,
    LOWEST_PRIORITY_TASK
)
from tasks.models import Task


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
