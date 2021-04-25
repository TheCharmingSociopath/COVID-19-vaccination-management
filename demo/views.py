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
    # process csv into a list called lst
    # bind lst to request and return
    return render(request, "statewise-covid-stats.html")

def StateVaccineStatsView(request):
    # download csv that has vaccination details
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

## END OF SARTHAK AREA

## =======================================================================

## BANSAL AREA

def CheckEligibilityFormView(request):
    if request.method == 'POST':
        form = CheckEligibilityForm(request.POST, request.FILES)
        if form.is_valid():
            # process form
            return HttpResponseRedirect(reverse('CheckEligibilityResult')) ## Redirect to the page with a form
        else:
            # error page
            pass
    else: # GET request
        default_adhaar = "666"
        form = CheckEligibilityForm(initial={"adhaar" : default_adhaar})
        return render(request, "check-eligibility-form.html", {'form' : form})

def CheckEligibilityResultView(request):
    return render(request, "check-eligibility-result.html")

## END OF BANSAL AREA
