import factory
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'user%d' % n)
    email = factory.LazyAttribute(lambda obj: '%s@elenas.co' % obj.username)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True
