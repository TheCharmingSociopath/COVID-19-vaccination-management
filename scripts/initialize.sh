#!/bin/bash

## Get the files
wget "http://api.covid19india.org/csv/latest/cowin_vaccine_data_statewise.csv"
wget "https://api.covid19india.org/csv/latest/state_wise.csv"
wget "https://api.covid19india.org/csv/latest/district_wise.csv"
wget "http://api.covid19india.org/csv/latest/cowin_vaccine_data_districtwise.csv"

## Update States database from CSV
python3 ../populate_State_District_models.py

## Update Districts database

## Setup dummy VaccinationCenter database

## Setup dummy CenterVaccinationStore database

python3 ../populate_VaccinationCenter_CenterVaccinationStore.py

## Setup dummy Population database
python3 ../populate_Population_model.py
