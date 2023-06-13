'''
    # https://faker.readthedocs.io/en/master/
    $ pip install faker # install faker module
    python manage.py flush # delete all exists data from db. dont forget: createsuperuser
    python manage.py shell
    from bank_app.faker import run
    run()
    exit()
'''

from .models import Transaction
from django.contrib.auth.models import User
import random
from faker import Faker
from django.utils.timezone import datetime, now
from pytz import timezone as tz


def add_user():
    fake = Faker()
    for _ in range(10):
        user = User()
        user.first_name = fake.first_name()
        user.last_name = fake.last_name()
        user.email = fake.free_email() 
        user.username = user.email
        user.set_password("qazqwe123")
        user.save()
    print('Users created')

def add_trx():
    qs_user = User.objects.all()
    
    fake = Faker()

    bulk_trx = []
    
    for i in range(100):
        data = {}
        user = random.randint(0,len(qs_user)-1)
        data["customer"] = qs_user[user]
        data["date"] = tz("UTC").localize(fake.date_time_between(
            start_date=datetime(2023, 3, 1),
            end_date=now()
        ))
        data["description"] = fake.text(max_nb_chars=50)
        data["amount"] = random.uniform(-1000, 1000)

        bulk_trx.append(Transaction(**data))

    Transaction.objects.bulk_create(bulk_trx)
      
    print("Fake transactions added")

def run():
    print('Fake data generation started')
    add_user()
    add_trx()
    print('Fake data generation completed')