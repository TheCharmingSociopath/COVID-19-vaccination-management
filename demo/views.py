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
    data = pd.read_csv('state_wise.csv', sep=',')
    row_iter = data.iterrows()
    States.objects.all().delete()
    STATES = [
            States(
                name = row['State'],
                number_of_active_cases = row['Active'],
                )
                for index, row in row_iter
    ]
    States.objects.bulk_create(STATES)

    data = pd.read_csv('state_wise.csv')
    data = data[['State_code','Active']]
    # data.drop(['State'])
    data.to_csv('static/files/active_map.csv', index = False)
    # data.to_csv('assets/files/active_map.csv', index = False)
    # process csv into a list called lst
    # bind lst to request and return
    return render(request, "statewise-covid-stats.html")

def StateVaccineStatsView(request):
    # download csv that has vaccination details
    # console.log("bakaa")
    data = pd.read_csv('cowin_vaccine_data_statewise.csv', sep=',')
    row_iter = data.iterrows()
    States.objects.all().delete()
    STATES = [
            States(
                name = row['State'],
                number_of_active_cases = row['Total Individuals Vaccinated'],
                )
                for index, row in row_iter 
    ]
    States.objects.bulk_create(STATES)

    data = pd.read_csv('cowin_vaccine_data_statewise.csv')
    data = data[['State_code','Total Individuals Vaccinated']]
    # data.drop(['State'])
    data.to_csv('static/files/active_map_vaccinated.csv', index = False)
    # process csv into a list called lst
    # bind lst to request and return
    return render(request, "statewise-vaccination-stats.html")

def DistrictwiseCovidStatsView(request): # How many vaccinated
    # download csv that has covid case details
    # process csv into a list called lst
    # bind lst to request and return
    return render(request, "districtwise-covid-stats.html")

def DistrictwiseVaccineStatsView(request):
    # download csv that has vaccination details
    # process csv into a list called lst
    # bind lst to request and return
    return render(request, "districtwise-vaccination-stats.html")

def VaccinationCentre(request):
    # download csv that has vaccination details
    # process csv into a list called lst
    # bind lst to request and return
    if request.method == 'POST':
        # form = CheckAadarNumber  ye baad me kardena warna merge conflict 
        return HttpResponseRedirect(reverse('VaccineCentreUpdateStatus'))
    else:
        return render(request, "vaccine-centre-index.html")

def VaccineCentreUpdateStatus(request):
    return render(request, "vaccine-centre-update-status.html")

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
            district = data['district']
            # if True
            url = 'EligibleForVaccine'
            return HttpResponseRedirect(reverse(url,args=[district, aadhar])) ## Redirect to the page with a form
            # else:
            #     return HttpResponseRedirect(reverse('NotEligibleForVaccine'))
        else:
            # error page
            pass
    else: # GET request
        form = CheckEligibilityForm()
        return render(request, "check-eligibility-form.html", {'form' : form})

def EligibleForVaccine(request, district, aadhar):
    #function to get list of vaccine centers from 
    
    vaccine_centers = ['cen1','cen2','cen3']
    return render(request, "eligible-for-vaccine.html", {'aadhar' : aadhar, 'district' : district, 'vaccine_centers' : vaccine_centers})

def NotEligibleForVaccine(request):
    return render(request, "not-eligible-for-vaccine.html")


## END OF BANSAL AREA
