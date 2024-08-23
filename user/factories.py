import factory
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    email = factory.Faker("email")
    password = factory.LazyFunction(
        lambda: make_password(
            factory
            .Faker("password")
            .evaluate(None, None, {"locale": None})
        )
    )

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)
