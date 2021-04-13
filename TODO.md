# TODO

## Pages

- Home
  - Statistics -- How many vaccinated, according to state -- Static
  - Eligibility for vaccination -- FormView (ID, Location)
    - Register for vaccination button, redirects to form for choosing center.
      - Give a date.
    - Otherwise, sorry not eligible.
  - Covid statistics -- Static
  - Currently active priority -- On home

- Admin
  - Manufacturing site -> Vaccination center table

- Vaccination Center
  - Vaccinated status update (Update status of ID, decreace count by 1)
  - Request for more vaccines

## Helpers

- CheckEligibility() -> bool
- VaccineAvailabilityInLocation()

## Models

### Population

- ID, Name, Age, Address, Profession, Priority, Vaccination status, Registration status, Scheduled time

### Vaccination Center

- Location, Number of vaccines

### Vaccine production

- Manufacturing site address, Number of doses

### Location

- Number of active cases, Number of vaccines

### Vaccination plan

- Currently active priority
