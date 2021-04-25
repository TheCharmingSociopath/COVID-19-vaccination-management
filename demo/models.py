from django.db import models

# Create your models here.

class States(models.Model):
    name = models.CharField(max_length=255)
    number_of_active_cases = models.IntegerField()

class Vaccinated(models.Model):
    name = models.CharField(max_length=255)
    number_of_vaccinated = models.IntegerField()

class Districts(models.Model):
    name = models.CharField(max_length=255)
    number_of_active_cases = models.IntegerField()
    state = models.ForeignKey(States, on_delete=models.CASCADE)

class Population(models.Model):
    vaccination_status_choices = (("unregistered", "Unregistered"), ("registered_1", "Registered for Dose 1"), ("registered_2", "Registered for Dose 2"), ("vaccinated", "Vaccinated"))
    profession_choices = (("medical_worker", "Medical Worker"), ("teacher", "Teacher"))
    adhaar = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    address = models.CharField(max_length=1023)
    district = models.ForeignKey(Districts, on_delete=models.CASCADE)
    state = models.ForeignKey(States, on_delete=models.CASCADE)
    profession = models.CharField(max_length=255, choices=profession_choices)
    priority = models.IntegerField()
    vaccination_status = models.CharField(max_length=255, choices=vaccination_status_choices)
    vaccine_1_time = models.DateTimeField()
    vaccine_2_time = models.DateTimeField()

class VaccinationCenter(models.Model):
    district = models.ForeignKey(Districts, on_delete=models.CASCADE)
    state = models.ForeignKey(States, on_delete=models.CASCADE)
    number_of_vaccines = models.IntegerField()
    address = models.CharField(max_length=1023)

class ManufacturingSite(models.Model):
    district = models.ForeignKey(Districts, on_delete=models.CASCADE)
    state = models.ForeignKey(States, on_delete=models.CASCADE)
    number_of_vaccines = models.IntegerField()
    address = models.CharField(max_length=1023)

