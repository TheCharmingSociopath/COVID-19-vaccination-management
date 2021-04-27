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
    district = forms.CharField(label = 'district', max_length = 100)

