import random

from django.core.management.base import BaseCommand
from django_seed import Seed
from faker import Faker

from payment.models import PaymentRequisite, PaymentRequest
from users.models import User

fake = Faker()
seeder = Seed.seeder()


class Command(BaseCommand):
    help = 'Seed the database with fake data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Seeding data...'))

        seeder.add_entity(User, 100, {
            'email': lambda x: fake.email(),
            'is_active': True,
            'email_verification_token': '',
            'phone': lambda x: fake.phone_number(),
            'avatar': None,
            'country': lambda x: fake.country(),
        })

        users = seeder.execute()[User]

        seeder.add_entity(PaymentRequisite, 100, {
            'user': lambda x: random.choice(users),
            'payment_type': lambda x: random.choice(['Card', 'BankAccount']),
            'account_type': lambda x: fake.word(),
            'owner_name': lambda x: fake.name(),
            'phone_number': lambda x: fake.phone_number(),
            'limit': lambda x: round(random.uniform(0.01, 10.0), 2),
        })

        seeder.add_entity(PaymentRequest, 5000, {
            'user': lambda x: random.choice(users),
            'amount': lambda x: round(random.uniform(1.0, 1000.0), 2),
            'status': lambda x: random.choice(['Pending', 'Paid', 'Cancelled']),
            'requisites': lambda x: random.choice(PaymentRequisite.objects.all()),
        })

        users = User.objects.all()

        user_objects = {user.id: user for user in users}

        for requisite in PaymentRequisite.objects.all():
            requisite.user = user_objects.get(requisite.user_id)
            requisite.save()

        seeder.execute()

        self.stdout.write(self.style.SUCCESS('Data seeding completed.'))
