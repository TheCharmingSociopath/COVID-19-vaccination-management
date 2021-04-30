from django.db import models
from django.utils import timezone
from django import forms
# from .models import model_name 

class CheckEligibilityForm(forms.Form):
    # in case you need to create a custom constructor for some form (like for getting data from a database)
    # def __init__(self, *args, **kwargs):
    #     self.some_field = tuple([(payload.id, payload.version) for payload in Model_Name.objects.filter(some_field=kwargs.pop('some_field_value'), deleted=False)])
    #     super(CheckEligibilityForm, self).__init__(*args, **kwargs)

    aadhar = forms.CharField(max_length=20)
    district_id = forms.IntegerField(label = 'district_id')


class RegisterForVaccine(forms.Form):
    centre = forms.CharField(max_length = 300)
    date = forms.DateField()
    time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))

class AdminForm(forms.Form):
    vaccine_number = forms.IntegerField()

class UpdateVaccineForm(forms.Form):
    aadhar = forms.CharField(max_length=20)
    centre_id = forms.CharField(max_length=20)
    status = forms.CharField(max_length=20)
 