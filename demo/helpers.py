from models.py import *
from collections import Counter
from datetime import timedelta, datetime

CURRENT_ACTIVE_PRIORITY = 1
STATES = ['IN-AN', 'IN-AP', 'IN-AR', 'IN-AS', 'IN-BR', 'IN-CH', 'IN-CT', 'IN-DN', 'IN-DL', 'IN-GA', 'IN-GJ', 'IN-HR', 'IN-HP', 'IN-JK', 'IN-JH', 'IN-KA', 'IN-KL', 'IN-LA', 'IN-LD', 'IN-MP', 'IN-MH', 'IN-MN', 'IN-ML', 'IN-MZ', 'IN-NL', 'IN-OR', 'IN-PY', 'IN-PB', 'IN-RJ', 'IN-SK', 'IN-TN', 'IN-TG', 'IN-TR', 'IN-UP', 'IN-UT', 'IN-WB']
LAST_DISPATCH = 0
PREVIOUS_ACTIVE_CASES = {}
WEIGHT1 = 0.6 # Ratio of Population
WEIGHT2 = 0.1 # Ratio of number of vaccination center per unit population
WEIGHT3 = 0.3 # Gradient of active cases

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
    center_list = {center.id : center.address for center in VaccinationCenter.objects.filter(district=district, deleted=False) if center.number_of_vaccines > 0}
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
    statewise_population, r1 = StatewisePopulation()
    r2 = StatewiseVaccinationCenterPopulationRatio(statewise_population)
    r3 = StatewiseInfectionGradient()
    r = { key : WEIGHT1 * r1[key] + WEIGHT2 * r2[key] + WEIGHT3 * r3[key] for key in r1 }
    print("sum of ratio", sum(list(r.values())))
    distribution = { key : r[key] * number for key in r }
    rem = number - sum(list(distribution.values()))
    print("rem: ", rem)
    distribution[STATES[-1]] += rem
    return distribution

def StatewisePopulation():
    lst = [person.state.state_code for person in Population.objects.all() if person.priority <= CURRENT_ACTIVE_PRIORITY and person.vaccination_status != "vaccinated"]
    statewise_population = dict(Counter(lst))
    return statewise_population, Normalise(ret)

def StatewiseVaccinationCenterPopulationRatio(statewise_population):
    lst = [center.state.state_code for center in VaccinationCenter.objects.all()]
    vccount = dict(Counter(lst))
    ret = { key : vccount[key] / statewise_population[key] for key in vccount}
    return Normalise(ret)

def StatewiseInfectionGradient():
    number_of_active_cases = {state.state_code : state.number_of_active_cases for state in States.objects.all() }

    PREVIOUS_ACTIVE_CASES = number_of_active_cases
    if LAST_DISPATCH == 0: # Return the current infection count the first time
        LAST_DISPATCH = datetime.now()
        return number_of_active_cases
    ## Return gradient number of active cases otherwise
    number_of_days = (datetime.now() - LAST_DISPATCH).days
    grad = { key : (number_of_active_cases[key] - PREVIOUS_ACTIVE_CASES[key]) / number_of_days for key in STATES }
    return Normalise(grad)

def Normalise(dick):
    total = 0
    for key in dick:
        total += dick[key]
    for key in dick:
        dick[key] /= total
    return dick
