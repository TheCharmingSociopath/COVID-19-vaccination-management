from .models import *
from collections import Counter
from datetime import timedelta, datetime
import copy


CURRENT_ACTIVE_PRIORITY = 1
LAST_DISPATCH = 0
STATES = ['IN-AN', 'IN-AP', 'IN-AR', 'IN-AS', 'IN-BR', 'IN-CH', 'IN-CT', 'IN-DN', 'IN-DL', 'IN-GA', 'IN-GJ', 'IN-HR', 'IN-HP', 'IN-JK', 'IN-JH', 'IN-KA', 'IN-KL', 'IN-LA', 'IN-LD', 'IN-MP', 'IN-MH', 'IN-MN', 'IN-ML', 'IN-MZ', 'IN-NL', 'IN-OR', 'IN-PY', 'IN-PB', 'IN-RJ', 'IN-SK', 'IN-TN', 'IN-TG', 'IN-TR', 'IN-UP', 'IN-UT', 'IN-WB']
PREVIOUS_ACTIVE_CASES = {}
WEIGHT1 = 0.6 # Ratio of Population
WEIGHT2 = 0.1 # Ratio of number of vaccination center per unit population
WEIGHT3 = 0.3 # Gradient of active cases

def CheckEligibilityHelper(aadhar, district):
    priority = Population.objects.filter(adhaar=aadhar)[0].priority
    print("priority = ", priority)
    if priority <= GetCurrentPriority(district):
        return True
    return False

def GetCurrentPriority(district):
    return CURRENT_ACTIVE_PRIORITY

def UpdatePriority(priority):
    CURRENT_ACTIVE_PRIORITY = priority

def VaccineAvailabilityInDistrict(district_id):
    center_list = {center.id : center.address for center in VaccinationCenter.objects.filter(district_id=district_id) if center.number_of_vaccines > 0}
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
    distribution = { key : round(r[key] * number) for key in r }
    rem = number - sum(list(distribution.values()))
    distribution[STATES[-1]] += rem
    print("done here")
    for state in STATES:
        new_vaccs = States.objects.get(state_code=state).number_of_vaccines + distribution[state]
        States.objects.filter(state_code=state).update(number_of_vaccines=new_vaccs)
    
    new_vaccines = CenterVaccinationStore.objects.all()[0].number_of_vaccines - number
    CenterVaccinationStore.objects.all().update(number_of_vaccines=new_vaccines)
    # return distribution

def StatewisePopulation():
    lst = []
    for person in Population.objects.all():
        if person.priority <= CURRENT_ACTIVE_PRIORITY and person.vaccination_status != "vaccinated":
            lst.append(person.state.state_code)
    statewise_population = dict(Counter(lst))
    for key in STATES:
        if key not in statewise_population:
            statewise_population[key] = 5
    return statewise_population, Normalise(copy.deepcopy(statewise_population))

def StatewiseVaccinationCenterPopulationRatio(statewise_population):
    lst = [center.state.state_code for center in VaccinationCenter.objects.all()]
    vccount = dict(Counter(lst))
    ret = { key : vccount[key] / statewise_population[key] for key in vccount}
    return Normalise(ret)

def StatewiseInfectionGradient():
    global LAST_DISPATCH, PREVIOUS_ACTIVE_CASES
    number_of_active_cases = {state.state_code : state.number_of_active_cases for state in States.objects.all() }

    if LAST_DISPATCH == 0: # Return the current infection count the first time
        PREVIOUS_ACTIVE_CASES = number_of_active_cases
        LAST_DISPATCH = datetime.now()
        return Normalise(number_of_active_cases)
    ## Return gradient number of active cases otherwise
    number_of_days = (datetime.now() - LAST_DISPATCH).days + 5
    grad = { key : (number_of_active_cases[key]+5 - PREVIOUS_ACTIVE_CASES[key]) / (number_of_days) for key in STATES }
    PREVIOUS_ACTIVE_CASES = number_of_active_cases
    LAST_DISPATCH = datetime.now()
    return Normalise(grad)

def Normalise(dick):
    total = 0
    for key in dick:
        total += dick[key]
    for key in dick:
        dick[key] /= total
    return dick

def GetListOfDistricts():
    lst = { district.name : district.pk for district in Districts.objects.all() }
    return lst

def GetStateWiseDistribution():
    ret = []
    population, _ = StatewisePopulation()
    for st in STATES:
        state = States.objects.get(state_code=st)
        ret.append({
            'state_name' : state.name,
            'population' : population[st],
            'active_case' : state.number_of_active_cases,
            'number_of_people_vaccinated' : state.number_of_people_vaccinated,
            'number_of_vaccine_available' : state.number_of_vaccines
        })
    return ret

def GetCenterVaccinationStore():
    return CenterVaccinationStore.objects.all()[0].number_of_vaccines

def GetCentreAddress(centre):
    #get centre address from id
    pass

def BookAppointmentAtVaccineCentre(centre,date,time,aadhar):
    #book appointment
    pass


def UpdateVaccinationDate(aadhar, date):
    pass