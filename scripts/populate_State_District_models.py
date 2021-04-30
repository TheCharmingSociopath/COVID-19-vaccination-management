import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','VaccineDistribution.settings')

import django
django.setup()

from demo.models import States, Districts
import csv, random, string

STATES = ['IN-AN', 'IN-AP', 'IN-AR', 'IN-AS', 'IN-BR', 'IN-CH', 'IN-CT', 'IN-DN', 'IN-DL', 'IN-GA', 'IN-GJ', 'IN-HR', 'IN-HP', 'IN-JK', 'IN-JH', 'IN-KA', 'IN-KL', 'IN-LA', 'IN-LD', 'IN-MP', 'IN-MH', 'IN-MN', 'IN-ML', 'IN-MZ', 'IN-NL', 'IN-OR', 'IN-PY', 'IN-PB', 'IN-RJ', 'IN-SK', 'IN-TN', 'IN-TG', 'IN-TR', 'IN-UP', 'IN-UT', 'IN-WB']

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
        _, _ = States.objects.get_or_create(name=name, number_of_active_cases=number_of_active_cases, number_of_people_vaccinated=number_of_people_vaccinated, number_of_vaccines=number_of_vaccines, state_code=state)

def PopulateDistrict(n):
    sids = [state for state in States.objects.all()]
    for i in range(n):
        name = ''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(20))
        number_of_active_cases = random.randint(100, 100000)
        state = random.choice(sids)
        _, _ = Districts.objects.get_or_create(name=name, number_of_active_cases=number_of_active_cases, state=state)

if __name__ == "__main__":
    PopulateState()
    PopulateDistrict(100)
