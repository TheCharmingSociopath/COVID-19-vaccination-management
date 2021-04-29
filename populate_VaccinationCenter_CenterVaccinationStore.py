import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','VaccineDistribution.settings')

import django
django.setup()

from demo.models import States, Districts, VaccinationCenter, CenterVaccinationStore
import random, string

def PopulateVaccinationCenter(n):
    sids = [state for state in States.objects.all()]
    dids = [district for district in Districts.objects.all()]
    for i in range(n):
        district = random.choice(dids)
        state = random.choice(sids)
        number_of_vaccines = random.randint(0, 100)
        address = ''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(50))
        _, _ = VaccinationCenter.objects.get_or_create(district=district, state=state, number_of_vaccines=number_of_vaccines, address=address)

def PopulateCenterVaccinationStore():
    # sids = [state.id for state in States.objects.all()]
    # dids = [district.id for district in Districts.objects.all()]
    # district = models.ForeignKey(Districts, on_delete=models.CASCADE)
    # state = models.ForeignKey(States, on_delete=models.CASCADE)
    number_of_vaccines = 10000
    # address = models.CharField(max_length=1023)
    _, _ = CenterVaccinationStore.objects.get_or_create(number_of_vaccines=number_of_vaccines)

if __name__ == "__main__":
    PopulateCenterVaccinationStore()
    PopulateVaccinationCenter(1000)
