from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from .helpers import *
from .forms import *
from .models import *


# Create your views here.
def HomeView(request):
    return render(request, "home.html")

## SARTHAK AREA
## Use helpers.py for all accessory functions
def StatewiseCovidStatsView(request): # How many vaccinated
    # download csv that has covid case details
    PrepareStateCovidCasesActiveMap()
    return render(request, "statewise-covid-stats.html")

def StateVaccineStatsView(request):
    # download csv that has vaccination details
    PrepareStateVaccinatedActiveMap()
    return render(request, "statewise-vaccination-stats.html")

def DistrictwiseCovidStatsView(request): # How many vaccinated
    # download csv that has covid case details
    # process csv into a list called lst
    # bind lst to request and return
    PrepareDistrictCovidCasesActiveMap()
    return render(request, "districtwise-covid-stats.html")

def DistrictwiseVaccineStatsView(request):
    # download csv that has vaccination details
    # process csv into a list called lst
    # bind lst to request and return
    PrepareDistrictVaccinatedActiveMap()
    return render(request, "districtwise-vaccination-stats.html")

def VaccinationCentre(request):
    # download csv that has vaccination details
    # process csv into a list called lst
    # bind lst to request and return
    if request.method == 'POST':
        form = UpdateVaccineForm(request.POST, request.FILES)
        if form.is_valid():
            # process form
            data = form.cleaned_data
            aadhar = data['aadhar']
            centre_id = data['centre_id']
            status = data['status']
            url = 'VaccineCentreUpdateStatus'
            # reduce vaccine count by one
            ReduceVaccineCountAtCenter(centre_id)
            UpdateVaccinationDate(aadhar, datetime.now())
            return HttpResponseRedirect(reverse(url,args=[aadhar, centre_id, status])) 
        else:
            pass
    else:
        return render(request, "vaccine-centre-index.html")


def VaccineCentreUpdateStatus(request, aadhar, centre_id, status):
    state_name = GetState(centre_id)
    return render(request, "vaccine-centre-update-status.html", {"aadhar":aadhar, "centre_id":centre_id, "status":status, "state_name" : state_name})

## END OF SARTHAK AREA

## =======================================================================

## BANSAL AREA

def CheckEligibilityFormView(request):
    if request.method == 'POST':
        form = CheckEligibilityForm(request.POST, request.FILES)
        if form.is_valid():
            # process form
            data = form.cleaned_data
            aadhar = data['aadhar']
            district_id = data['district_id']
            if AadharExists(aadhar):
                if CheckEligibilityHelper(aadhar, district_id):
                    url = 'EligibleForVaccine'
                    return HttpResponseRedirect(reverse(url,args=[district_id, aadhar])) ## Redirect to the page with a form
                else:
                    return HttpResponseRedirect(reverse('NotEligibleForVaccine',args=[1]))
            else:
                return HttpResponseRedirect(reverse('NotEligibleForVaccine',args=[2]))
        else:
            pass
    else: # GET request
        form = CheckEligibilityForm()
        district = GetListOfDistricts()
        return render(request, "check-eligibility-form.html", {'form' : form, 'district' : district})

def EligibleForVaccine(request, district_id, aadhar):
    if request.method == 'POST':
        form = RegisterForVaccine(request.POST, request.FILES)
        if form.is_valid():
            # process form
            data = form.cleaned_data
            centre = data['centre']
            date = data['date']
            time = data['time']
            return HttpResponseRedirect(reverse('AppointmentBooked',args=[centre,date,time,aadhar])) ## Redirect to the page with a form
        else:
            # error page
            pass
    else: # GET request
        form = RegisterForVaccine()    
        vaccine_centers = VaccineAvailabilityInDistrict(district_id)
        return render(request, "eligible-for-vaccine.html", {'aadhar' : aadhar, 'district_id' : district_id, 'vaccine_centers' : vaccine_centers})

def NotEligibleForVaccine(request, flag):
    return render(request, "not-eligible-for-vaccine.html", {'flag' : flag})

def AppointmentBookedView(request,centre,date,time,aadhar):
    centre_add = GetCentreAddress(centre)
    time = time[:-3]
    BookAppointmentAtVaccineCentre(centre,date,time,aadhar)
    return render(request, "appointment-booked.html", {'centre_add' : centre_add, 'date' : date, 'time' : time})

def AdminDistributeView(request):
    global CURRENT_ACTIVE_PRIORITY
    if request.method == 'POST':
        form = AdminForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            vaccine_number = data['vaccine_number']
            priority = data['priority']
            SetCurrentActivePriority(priority)
            DistributeCenterToState(vaccine_number)
            return HttpResponseRedirect(reverse('admin')) ## Redirect to the page with a form
        else:
            pass
    else: # GET request
        centre_vaccine_count = GetCenterVaccinationStore()
        return render(request, "admin-distribute.html", {'centre_vaccine_count': centre_vaccine_count, 'current_active_priority' : CURRENT_ACTIVE_PRIORITY, 'range' : range(1, 5)})


def AdminView(request):
    centre_vaccine_count = GetCenterVaccinationStore()
    state_data = GetStateWiseDistribution()
    return render(request, "admin.html", {'state_data': state_data, 'centre_vaccine_count': centre_vaccine_count})

## END OF BANSAL AREA
