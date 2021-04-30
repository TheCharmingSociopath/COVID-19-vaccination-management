import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','VaccineDistribution.settings')

import django
django.setup()

from demo.models import States, Districts, Population, VaccinationCenter, CenterVaccinationStore
import random, string, uuid, csv
from datetime import datetime


STATES = ['IN-AN', 'IN-AP', 'IN-AR', 'IN-AS', 'IN-BR', 'IN-CH', 'IN-CT', 'IN-DN', 'IN-DL', 'IN-GA', 'IN-GJ', 'IN-HR', 'IN-HP', 'IN-JK', 'IN-JH', 'IN-KA', 'IN-KL', 'IN-LA', 'IN-LD', 'IN-MP', 'IN-MH', 'IN-MN', 'IN-ML', 'IN-MZ', 'IN-NL', 'IN-OR', 'IN-PY', 'IN-PB', 'IN-RJ', 'IN-SK', 'IN-TN', 'IN-TG', 'IN-TR', 'IN-UP', 'IN-UT', 'IN-WB']

def PopulateVaccinationCenter(n):
    sids = [state for state in States.objects.all()]
    dids = [district for district in Districts.objects.all()]
    for i in range(n):
        district = random.choice(dids)
        state = random.choice(sids)
        number_of_vaccines = random.randint(0, 100)
        address = ''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(50))
        _, _ = VaccinationCenter.objects.get_or_create(district=district, state=state, number_of_vaccines=number_of_vaccines, address=address)

def PopulateCenterVaccinationStore():
    # sids = [state.id for state in States.objects.all()]
    # dids = [district.id for district in Districts.objects.all()]
    # district = models.ForeignKey(Districts, on_delete=models.CASCADE)
    # state = models.ForeignKey(States, on_delete=models.CASCADE)
    number_of_vaccines = 10000
    # address = models.CharField(max_length=1023)
    _, _ = CenterVaccinationStore.objects.get_or_create(number_of_vaccines=number_of_vaccines)

def PopulateState():
    vac = {}
    cases = {}
    names = {}
    with open('cowin_vaccine_data_statewise.csv', 'r') as fil:
        reader = csv.reader(fil)
        rows = list(reader)
        rows.pop(0)
        rows.pop(0)
        for state in rows:
            code = state[2]
            for s in STATES:
                # if s[3:] == code:
                if s == code:
                    vac[s] = state[-2]
                    names[s] = state[1]

    with open('state_wise.csv', 'r') as fil:
        reader = csv.reader(fil)
        rows = list(reader)
        rows.pop(0)
        rows.pop(0)
        for state in rows:
            code = state[-5]
            for s in STATES:
                # if s[3:] == code:
                if s == code:
                    cases[s] = state[4]
    
    for state in STATES:
        name = names[state]
        number_of_active_cases = cases[state]
        number_of_vaccines = 0
        number_of_people_vaccinated = vac[state]
        state_code = state
        _, _ = States.objects.get_or_create(name=name, number_of_active_cases=number_of_active_cases, number_of_people_vaccinated=number_of_people_vaccinated, number_of_vaccines=number_of_vaccines, state_code=state_code)

def PopulateDistrict(n):
    sids = [state for state in States.objects.all()]
    for i in range(n):
        name = ''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(20))
        number_of_active_cases = random.randint(100, 100000)
        state = random.choice(sids)
        _, _ = Districts.objects.get_or_create(name=name, number_of_active_cases=number_of_active_cases, state=state)

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
    PopulateState()
    PopulateDistrict(1000)
    PopulatePopulation(10000)
    PopulateCenterVaccinationStore()
    PopulateVaccinationCenter(1000)
