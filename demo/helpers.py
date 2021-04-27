from models.py import *
from collections import Counter

CURRENT_ACTIVE_PRIORITY = 1
STATES = ['IN-AN', 'IN-AP', 'IN-AR', 'IN-AS', 'IN-BR', 'IN-CH', 'IN-CT', 'IN-DN', 'IN-DL', 'IN-GA', 'IN-GJ', 'IN-HR', 'IN-HP', 'IN-JK', 'IN-JH', 'IN-KA', 'IN-KL', 'IN-LA', 'IN-LD', 'IN-MP', 'IN-MH', 'IN-MN', 'IN-ML', 'IN-MZ', 'IN-NL', 'IN-OR', 'IN-PY', 'IN-PB', 'IN-RJ', 'IN-SK', 'IN-TN', 'IN-TG', 'IN-TR', 'IN-UP', 'IN-UT', 'IN-WB']

def CheckEligibilityHelper(aadhar, district):
    priority = Population.objects.filter(adhaar=aadhar, deleted=False)
    if priority <= GetCurrentPriority(district):
        return True
    return False

def GetCurrentPriority(district):
    return CURRENT_ACTIVE_PRIORITY

def UpdatePriority(priority):
    CURRENT_ACTIVE_PRIORITY = priority

def VaccineAvailabilityInDistrict(district):
    center_list = [{'id' : center.id, 'address' : center.address} for center in VaccinationCenter.objects.filter(district=district, deleted=False) if center.number_of_vaccines > 0]
    return center_list

def ReduceVaccineCountAtCenter(center_id):
    center = VaccinationCenter.objects.get(pk=center_id)
    center.number_of_vaccines = center.number_of_vaccines - 1
    state = States.objects.get(pk=center.state)
    state.number_of_vaccines = state.number_of_vaccines - 1
    state.number_of_people_vaccinated = state.number_of_people_vaccinated + 1
    state.save()
    center.save()

def DistributeCenterToState(number):
    # weighted ratio of StatewisePopulation, StatewiseVaccinationCenterPopulationRatio, StatewiseInfectionGradient 
    pass

def GetTable():
    pass

def Initialize():
    # Update active cases in states database from CSV
    # Update active cases in districts database from CSV
    pass

def StatewisePopulation():
    lst = [person.state.state_code for person in Population.objects.all() if person.priority <= CURRENT_ACTIVE_PRIORITY]
    return dict(Counter(lst))

def StatewiseVaccinationCenterPopulationRatio(statewise_population):
    lst = [center.state.state_code for center in VaccinationCenter.objects.all()]
    vccount = dict(Counter(lst))
    ret = {}
    for key in vccount:
        ret[key] = vccount[key] / statewise_population[key]
    return ret

def StatewiseInfectionGradient():
    pass
