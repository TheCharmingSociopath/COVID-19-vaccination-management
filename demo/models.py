from django.db import models

# Create your models here.

class States(models.Model):
    state_codes = (('IN-AN', 'IN-AN'), ('IN-AP', 'IN-AP'), ('IN-AR', 'IN-AR'), ('IN-AS', 'IN-AS'), ('IN-BR', 'IN-BR'), ('IN-CH', 'IN-CH'), ('IN-CT', 'IN-CT'), ('IN-DN', 'IN-DN'), ('IN-DL', 'IN-DL'), ('IN-GA', 'IN-GA'), ('IN-GJ', 'IN-GJ'), ('IN-HR', 'IN-HR'), ('IN-HP', 'IN-HP'), ('IN-JK', 'IN-JK'), ('IN-JH', 'IN-JH'), ('IN-KA', 'IN-KA'), ('IN-KL', 'IN-KL'), ('IN-LA', 'IN-LA'), ('IN-LD', 'IN-LD'), ('IN-MP', 'IN-MP'), ('IN-MH', 'IN-MH'), ('IN-MN', 'IN-MN'), ('IN-ML', 'IN-ML'), ('IN-MZ', 'IN-MZ'), ('IN-NL', 'IN-NL'), ('IN-OR', 'IN-OR'), ('IN-PY', 'IN-PY'), ('IN-PB', 'IN-PB'), ('IN-RJ', 'IN-RJ'), ('IN-SK', 'IN-SK'), ('IN-TN', 'IN-TN'), ('IN-TG', 'IN-TG'), ('IN-TR', 'IN-TR'), ('IN-UP', 'IN-UP'), ('IN-UT', 'IN-UT'), ('IN-WB', 'IN-WB') )
    name = models.CharField(max_length=255)
    number_of_active_cases = models.IntegerField(default=0)
    number_of_vaccines = models.IntegerField(default=0)
    number_of_people_vaccinated = models.IntegerField(default=0)
    state_code = models.CharField(max_length=10, choices=state_codes, default="IN-AN")

class Districts(models.Model):
    name = models.CharField(max_length=255)
    number_of_active_cases = models.IntegerField(default=0)
    state = models.ForeignKey(States, on_delete=models.CASCADE)

class Population(models.Model):
    vaccination_status_choices = (("unregistered", "Unregistered"), ("registered_1", "Registered for Dose 1"), ("dose_1_administered", "Dose 1 administered"), ("registered_2", "Registered for Dose 2"), ("vaccinated", "Vaccinated"))
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
    vaccination_center_chosen = models.IntegerField(default=0)

class VaccinationCenter(models.Model):
    district = models.ForeignKey(Districts, on_delete=models.CASCADE)
    state = models.ForeignKey(States, on_delete=models.CASCADE)
    number_of_vaccines = models.IntegerField(default=0)
    address = models.CharField(max_length=1023)

class CenterVaccinationStore(models.Model):
    # district = models.ForeignKey(Districts, on_delete=models.CASCADE)
    # state = models.ForeignKey(States, on_delete=models.CASCADE)
    number_of_vaccines = models.IntegerField()
    # address = models.CharField(max_length=1023)
