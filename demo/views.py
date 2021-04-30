from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from .helpers import *
from .forms import *
from .models import *
import pandas as pd


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
        # form = CheckAadarNumber  ye baad me kardena warna merge conflict 
        form = UpdateVaccineForm(request.POST, request.FILES)
        if form.is_valid():
            # process form
            data = form.cleaned_data
            aadhar = data['aadhar']
            centre_id = data['centre_id']
            status = data['status']
            print(aadhar)
            url = 'VaccineCentreUpdateStatus'
            # reduce vaccine count by one
            # ReduceVaccineCountAtCenter(center_id)
            # UpdateVaccinationDate(aadhar, datetime.now)
            return HttpResponseRedirect(reverse(url,args=[aadhar, centre_id, status])) 
        else:
            pass
    else:
        return render(request, "vaccine-centre-index.html")


def VaccineCentreUpdateStatus(request, aadhar, centre_id, status):
    return render(request, "vaccine-centre-update-status.html", {"aadhar":aadhar, "centre_id":centre_id, "status":status})

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
            if CheckEligibilityHelper(aadhar, district_id):
                url = 'EligibleForVaccine'
                return HttpResponseRedirect(reverse(url,args=[district_id, aadhar])) ## Redirect to the page with a form
            else:
                return HttpResponseRedirect(reverse('NotEligibleForVaccine'))
        else:
            print("btbtbtbt")
            # error page
            # pass
    else: # GET request
        form = CheckEligibilityForm()
        district = GetListOfDistricts()
        print("district = ", district)
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
        #function to get list of vaccine centers from 
        form = RegisterForVaccine()    
        vaccine_centers = VaccineAvailabilityInDistrict(district_id)
        # print("centers = ",vaccine_centers)
        return render(request, "eligible-for-vaccine.html", {'aadhar' : aadhar, 'district_id' : district_id, 'vaccine_centers' : vaccine_centers})

def NotEligibleForVaccine(request):
    return render(request, "not-eligible-for-vaccine.html")

def AppointmentBookedView(request,centre,date,time,aadhar):
    #function to get centre address
    # centre_add = GetCentreAddress(centre)
    centre_add = "temp"
    #add this to database
    #BookAppointmentAtVaccineCentre(centre,date,time,aadhar)
    return render(request, "appointment-booked.html", {'centre_add' : centre_add, 'date' : date, 'time' : time})

def AdminDistributeView(request):
    print("distribute view called...")
    if request.method == 'POST':
        form = AdminForm(request.POST, request.FILES)
        if form.is_valid():
            # process form
            data = form.cleaned_data
            vaccine_number = data['vaccine_number']
            print("number = ", vaccine_number)
            DistributeCenterToState(vaccine_number)
            print("data updated")
            # return HttpResponseRedirect(reverse('admin')) ## Redirect to the page with a form
            return HttpResponseRedirect(reverse('admin')) ## Redirect to the page with a form
        else:
            # error page
            pass
    else: # GET request
        centre_vaccine_count = GetCenterVaccinationStore()
        return render(request, "admin-distribute.html", {'centre_vaccine_count': centre_vaccine_count})


def AdminView(request):
    print("admin view called...")
    centre_vaccine_count = GetCenterVaccinationStore()
    state_data = GetStateWiseDistribution()
    s = 0
    for st in state_data:
        s += st['number_of_vaccine_available']
    print("sum = ", s)
    return render(request, "admin.html", {'state_data': state_data, 'centre_vaccine_count': centre_vaccine_count})

## END OF BANSAL AREA
