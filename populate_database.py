import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','VaccineDistribution.settings')

import django
django.setup()

from demo.models import States, Districts, Population, VaccinationCenter, CenterVaccinationStore
import random, string, uuid, csv
from datetime import datetime


STATES = ['IN-AN', 'IN-AP', 'IN-AR', 'IN-AS', 'IN-BR', 'IN-CH', 'IN-CT', 'IN-DN', 'IN-DL', 'IN-GA', 'IN-GJ', 'IN-HR', 'IN-HP', 'IN-JK', 'IN-JH', 'IN-KA', 'IN-KL', 'IN-LA', 'IN-LD', 'IN-MP', 'IN-MH', 'IN-MN', 'IN-ML', 'IN-MZ', 'IN-NL', 'IN-OR', 'IN-PY', 'IN-PB', 'IN-RJ', 'IN-SK', 'IN-TN', 'IN-TG', 'IN-TR', 'IN-UP', 'IN-UT', 'IN-WB']
POPULATION = [417036, 53903393, 1570458, 35607039, 124799926, 1158473, 29436231, 615724, 18710922, 1586250, 63872399, 28204692, 7451955, 13606320, 38593948, 67562686, 35699443, 289023, 73183, 85358965, 123144223, 3091545, 3366710, 1239244, 2249695, 46356334, 1413542, 30141373, 81032689, 690251, 77841267, 39362732, 4169794, 237882725, 11250858, 99609303]

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
    
    for i in range(len(STATES)):
        state = STATES[i]
        population = POPULATION[i]
        name = names[state]
        number_of_active_cases = cases[state]
        number_of_vaccines = 0
        number_of_people_vaccinated = vac[state]
        state_code = state
        _, _ = States.objects.get_or_create(name=name, number_of_active_cases=number_of_active_cases, number_of_people_vaccinated=number_of_people_vaccinated, number_of_vaccines=number_of_vaccines, state_code=state, state_population=population)

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
    PopulateDistrict(100)
    PopulatePopulation(1000)
    PopulateCenterVaccinationStore()
    PopulateVaccinationCenter(1000)
    state = States.objects.get(state_code='IN-DL')
    district = Districts(name="Noida", number_of_active_cases=7542, state=state)
    district.save()
    shivam = Population(adhaar="111111111111", name="Shivam Bansal", age=20, address="Mukul Mahal, Gau Vihar Colony, Noida", district=district, state=state, profession="student", priority=4, vaccination_status="unregistered", vaccine_1_time=datetime.now(), vaccine_2_time=datetime.now(), vaccination_center_chosen=0)
    vacc = VaccinationCenter(district=district, state=state, number_of_vaccines=0, address="BT Hospital, Noida")
    shivam.save()
    vacc.save()
