"""
Factory Boy factories for generating test data.
"""

import factory
from factory.django import DjangoModelFactory
from faker import Faker
from apps.accounts.models import User, SystemConfig
from apps.contacts.models import Company, Contact
from apps.deals.models import Pipeline, Stage, Deal

fake = Faker()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("username")
    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    role = "rep"
    is_active = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        obj = model_class(*args, **kwargs)
        obj.set_password("testpassword123")
        obj.save()
        return obj


class SystemConfigFactory(DjangoModelFactory):
    class Meta:
        model = SystemConfig

    base_currency = "USD"
    default_timezone = "UTC"


class CompanyFactory(DjangoModelFactory):
    class Meta:
        model = Company

    name = factory.Faker("company")
    industry = factory.Faker("word")
    website = factory.Faker("url")
    phone = factory.Faker("phone_number")
    city = factory.Faker("city")
    state = factory.Faker("state")
    country = factory.Faker("country")
    is_active = True
    is_deleted = False


class ContactFactory(DjangoModelFactory):
    class Meta:
        model = Contact

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    phone = factory.Faker("phone_number")
    title = factory.Faker("job")
    company = factory.SubFactory(CompanyFactory)
    source = "inbound"
    is_active = True
    is_deleted = False


class PipelineFactory(DjangoModelFactory):
    class Meta:
        model = Pipeline

    name = factory.Sequence(lambda n: f"Pipeline {n}")
    type = "hunting"
    description = factory.Faker("sentence")


class StageFactory(DjangoModelFactory):
    class Meta:
        model = Stage

    pipeline = factory.SubFactory(PipelineFactory)
    name = factory.Sequence(lambda n: f"Stage {n}")
    order = factory.Sequence(lambda n: n)
    is_terminal = False


class TerminalStageFactory(StageFactory):
    name = factory.Faker("word")
    is_terminal = True


class DealFactory(DjangoModelFactory):
    class Meta:
        model = Deal

    pipeline = factory.SubFactory(PipelineFactory)
    current_stage = factory.SubFactory(StageFactory, pipeline=factory.SelfAttribute("..pipeline"))
    company = factory.SubFactory(CompanyFactory)
    contact = factory.SubFactory(ContactFactory, company=factory.SelfAttribute("..company"))
    title = factory.Faker("sentence")
    description = factory.Faker("paragraph")
    amount = factory.Faker("pydecimal", left_digits=6, right_digits=2, positive=True)
    currency = "USD"
    probability = factory.Faker("random_int", min=0, max=100)
    expected_close_date = factory.Faker("future_date")
    owner = factory.SubFactory(UserFactory)
    created_by = factory.SubFactory(UserFactory)
