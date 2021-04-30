# DM Report - Team 5

- Shivam Bansal  - 20171118
- Aditya Morolia - 20171177
- Sarthak Singh   - 20171118

## Introduction

Vaccine drives are expensive tasks, requiring many man-hours of planning and execution to achieve the desired task, often saving millions of human lives. In the past, the world has seen huge success while running huge vaccination drives for smallpox, polio, and many other such diseases, eliminating many of them along the way. We take the example of the ongoing challenge of vaccinating people for the COVID-19 infection to demonstrate some of the ways in which IT can help with the huge vaccination drive.

The development and widespread use of an effective SARS-CoV-2 vaccine could help prevent substantial morbidity and mortality associated with COVID-19 infection and mitigate many of the secondary effects associated with non-pharmaceutical interventions. The limited availability of an effective and licensed vaccine will task policymakers around the world, including in India, with decisions regarding optimal vaccine allocation strategies. [1] Here we present a web app that can help us manage the vaccination drive, by keeping track of various stages of the drive, helping in the analysis and planning of the drive, and deciding on a fair scheme to distribute vaccines from the center to various vaccination centers in the country.

## About the vaccination drive and our algorithm

Limited initial supply of severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2) vaccine raises the question of how to prioritize available doses. In a mathematical model, a highly effective transmission-blocking vaccine prioritized to adults ages 20 to 49 years minimized cumulative incidence (symptomatic cases), but mortality and years of life lost were minimized in most scenarios when the vaccine was prioritized to adults greater than 60 years old. [2] Here, we assume that the population is distributed in 4 categories, labeled from $\{1, 2, 3, 4\}$, and at each stage of the vaccination drive, for stage $i$, all the people with a priority $\leq i$ are eligible to receive a vaccine. We then formulate an algorithm to distribute a limited supply of $n$ vaccines from a vaccine store (which can be the central government or the state government) to a target set (various state governments or districts.) We then use an implementation of this in our portal to automate vaccine distribution from the center to the states. Due to the modularity of the codebase, this can easily be translated to be used in other situations, such as extending the use case by adding a feature to distribute the vaccines received by a state to the various districts in the state. 

## Algorithm to find a distribution of $n$  vaccines from a central store among $m$  states

Let $\{s_1, s_2, \ldots s_m\}$ be the states. 

We are taking into account the following three variables while distributing vaccines to the states. 

- Population in the current priority group living in the state

    This is given by the number of people in the state with priority `<= CURRENT_PHASE`

    Let this be $p_1, p_2, \ldots p_m$.

    Let $r_{11}, r_{12}, \ldots r_{1m}$ be the fraction of population eligible in the current phase in each state.

    That is, $r_{1i} = \frac{p_i}{\sum_j p_j}$

    This is considered because the state with a higher fraction should be given more vaccines to administer.

- The number of vaccination centres in the state, per unit population

    Let $v_1, v_2, \ldots v_m$ be the number of vaccination centres in each state.

    Then, the variable we take into account is $r_{2i} = \frac{v_i}{p_i}$

- The gradient of the number of active cases of COVID-19 infections in the state.

    To find this, we take the average increment in the number of cases in the state from a previous time instant to the current time instant.

    Let $d_1, d_2, \ldots d_m$ be the difference between the active infections in the states in $k$ days.

    Then, take $r_{3i}  = \frac{d_i}{k}$.

Now, we will use a convex mixture of these fractions to find a ratio in which to divide the $m$ vaccines. Let $w_1, w_2, w_3$ be the weights we want to use to combine the ratios $r_1, r_2, r_3$ such that $w_1 + w_2 + w_3 = 1$, then the final ratio will be given as $r = \{ \sum_j w_jr_{ji} \}_i$

We can then divide the $n$ vaccines among the $m$ states in the ratio $r_1, r_2, \ldots r_m$.

## Application functionalities/features:

In our application, we have provided several different functionalities for three different groups of people which include Admin, Vaccine centers, and the general public. The features of the general public are common to all, but the admin and vaccine centers get some exclusive features that are explained below:

![image1](/static/images/screenshots/1.png)

## Admin-

### 1. Analytics:

This functionality allows the user (with admin access) to view the name, population, the number of people vaccinated, and the number of vaccines available for every state in India in a tabular form. 

![image2](/static/images/screenshots/2.png)

### 2. Distribute Vaccines or Update Vaccination Phase:

Admin gets the stock of vaccines that are to be distributed throughout the country based on our algorithm to provide effective and efficient distribution of available vaccines.

![image3](/static/images/screenshots/3.png)

## Vaccine Centre-

### 1. Update vaccination status of an individual:

Vaccine Centers can also use our platform to update the status of vaccines administered to an individual (i.e. registered for dose 1, dose 1 administered, registered for dose 2, and completely vaccinated).

 ![image7](/static/images/screenshots/7.png)

### 2. Update vaccine count:

This helps keep track and update the number of vaccines that are available in that particular district, state, and the country (India) where the individual was administered.

## General Public-

### 1. Check Eligibility:

Since, there are a group of people i.e. healthcare workers, doctors, police, elderly, etc. who should be given priority over other groups. This feature helps to filter out those who can or cannot register for the vaccine due to the lack of the number of vaccines to vaccinate every person in the country.

![image4](/static/images/screenshots/4.png)

### 2. Register for vaccine and book an appointment:

Those who are eligible, can register for vaccine and book an appointment in the district of their choice, at their nearest center (User can choose from the centers available in your districts) at a time of their choice.

![image6](/static/images/screenshots/5.png) 

### 3. Heatmap Visualizations:

Two heatmaps of India, first, to track the active number of cases in each state and second, to track the number of people vaccinated in each state have been implemented. This feature updates dynamically when a new person is vaccinated in a particular state and the vaccine center updates the status of that person. 

![image8](/static/images/screenshots/8.png)

![image9](/static/images/screenshots/9.png)

# References:

[1] [[https://www.medrxiv.org/content/10.1101/2020.11.22.20236091v1.full](https://www.medrxiv.org/content/10.1101/2020.11.22.20236091v1.full)]([https://www.medrxiv.org/content/10.1101/2020.11.22.20236091v1.full](https://www.medrxiv.org/content/10.1101/2020.11.22.20236091v1.full))

[2] [[https://science.sciencemag.org/content/371/6532/916](https://science.sciencemag.org/content/371/6532/916)]([https://science.sciencemag.org/content/371/6532/916](https://science.sciencemag.org/content/371/6532/916))

[3][[https://www.who.int/docs/default-source/immunization/sage/covid/sage-prioritization-roadmap-covid19-vaccines.pdf](https://www.who.int/docs/default-source/immunization/sage/covid/sage-prioritization-roadmap-covid19-vaccines.pdf)]([https://www.who.int/docs/default-source/immunization/sage/covid/sage-prioritization-roadmap-covid19-vaccines.pdf](https://www.who.int/docs/default-source/immunization/sage/covid/sage-prioritization-roadmap-covid19-vaccines.pdf))

[4][[https://www.cdc.gov/vaccines/acip/meetings/downloads/slides-2020-08/COVID-08-Dooling.pdf](https://www.cdc.gov/vaccines/acip/meetings/downloads/slides-2020-08/COVID-08-Dooling.pdf)]([https://www.cdc.gov/vaccines/acip/meetings/downloads/slides-2020-08/COVID-08-Dooling.pdf](https://www.cdc.gov/vaccines/acip/meetings/downloads/slides-2020-08/COVID-08-Dooling.pdf))