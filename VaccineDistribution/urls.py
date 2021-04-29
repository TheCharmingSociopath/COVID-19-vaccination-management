"""VaccineDistribution URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from demo import views

urlpatterns = [
    path('', views.HomeView, name='home'),
    path('admin/', views.AdminView, name='admin'),
    path('adminDistribute/', views.AdminDistributeView, name='adminDistribute'),
    path('AppointmentBooked/<str:centre>/<str:date>/<str:time>/', views.AppointmentBookedView, name='AppointmentBooked'),
    path('StatewiseCovidStats/', views.StatewiseCovidStatsView, name='StatewiseCovidStats'),
    path('StateVaccineStats/', views.StateVaccineStatsView, name='StateVaccineStats'),
    path('DistrictwiseCovidStats/', views.DistrictwiseCovidStatsView, name='DistrictwiseCovidStats'),
    path('DistrictwiseVaccineStats/', views.DistrictwiseVaccineStatsView, name='DistrictwiseVaccineStats'),
    path('CheckEligibilityForm/', views.CheckEligibilityFormView, name='CheckEligibilityForm'),
    path('EligibleForVaccine/<int:district_id>/<str:aadhar>', views.EligibleForVaccine, name='EligibleForVaccine'),
    path('NotEligibleForVaccine/', views.NotEligibleForVaccine, name='NotEligibleForVaccine'),
    path('VaccinationCentre/', views.VaccinationCentre, name='VaccinationCentre'),
    path('VaccineCentreUpdateStatus/', views.VaccineCentreUpdateStatus, name='VaccineCentreUpdateStatus')
]
