#!/bin/bash

## Create vitualenv
mkvirtualenv covid-19-vac

## Install libraries
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate

## Get the files
wget "http://api.covid19india.org/csv/latest/cowin_vaccine_data_statewise.csv"
wget "https://api.covid19india.org/csv/latest/state_wise.csv"
wget "https://api.covid19india.org/csv/latest/district_wise.csv"
wget "http://api.covid19india.org/csv/latest/cowin_vaccine_data_districtwise.csv"

## Populate the database

python3 populate_database.py
