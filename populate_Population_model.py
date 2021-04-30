import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','VaccineDistribution.settings')

import django
django.setup()

from demo.models import States, Districts, Population
import random, string, uuid
from datetime import datetime

def PopulatePopulation(n):
    sids = [state for state in States.objects.all()]
    dids = [district for district in Districts.objects.all()]
    for i in range(n):
        profession_choices = ["medical_worker", "teacher", "engineer", "daily_wage_worker"]
        adhaar = str(uuid.uuid4())[-12:]
        name = ''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(20))
        age = random.randint(18, 95)
        address = ''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(50))
        district = random.choice(dids)
        state = random.choice(sids)
        profession = random.choice(profession_choices)
        priority = random.randint(1, 5)
        vaccination_status = "unregistered"
        vaccine_1_time = datetime.now()
        vaccine_2_time = datetime.now()
        _, _ = Population.objects.get_or_create(adhaar=adhaar, name=name, age=age, address=address, district=district, state=state, profession=profession, priority=priority, vaccination_status=vaccination_status, vaccine_1_time=vaccine_1_time, vaccine_2_time=vaccine_2_time)

if __name__ == "__main__":
    PopulatePopulation(1000)
