import requests, re, string
from datetime import datetime


class CovidMonitor:
    def __init__(self):
        self.__url = ""
        self.__headers = {
            'x-rapidapi-key': "50e6e2d878msh826a79e23a82f97p1a4c7fjsnc2f0b125bf1a",
            'x-rapidapi-host': "covid-193.p.rapidapi.com"
        }

    def countries(self) -> list:
        self.__url = "https://covid-193.p.rapidapi.com/countries"
        response = requests.request("GET", self.__url, headers=self.__headers)
        return response.json().get('response')

    def get_previous_cases(self, country, date) -> dict:
        self.__url = 'https://covid-193.p.rapidapi.com/history'
        query = {
            'country': country,
            'day': date
        }

        response = requests.request('GET', self.__url, headers=self.__headers, params=query)
        covid_response: dict = response.json().get('response')[0]
        cases: dict = covid_response.get('cases')

        chars = re.escape(string.punctuation)
        new = cases.get('new')
        new_cases = int(re.sub(f'[{chars}]', '', new)) if new is not None else 0

        deaths = covid_response.get('deaths').get('new')
        new_deaths = int(re.sub(f'[{chars}]', '', deaths)) if deaths is not None else 0

        results = {
            'Active': cases.get('active'),
            'New Cases': new_cases,
            'Deaths': new_deaths,
        }

        return results

    def search(self, country) -> dict:
        self.__url = "https://covid-193.p.rapidapi.com/statistics"
        country_query = {"country": country}

        response = requests.request("GET", self.__url, headers=self.__headers, params=country_query)
        covid_response: dict = response.json().get('response')[0]
        cases: dict = covid_response.get('cases')

        date = datetime.strptime(covid_response.get("day"), '%Y-%m-%d')
        date_ftd = datetime.strftime(date, '%A, %B %d, %Y')

        results = {
            'Date': date_ftd,
            'Country': covid_response.get('country'),
            'New Cases': cases.get('new'),
            'Active': cases.get('active'),
            'Recovered': cases.get('recovered'),
            'New Deaths': covid_response.get('deaths').get('new'),
            'Total Deaths': covid_response.get('deaths').get('total'),
            'Total': cases.get('total')
        }

        return results
    
# Datetime:
# %Y : Year (4 digits)
# %y : Year
# %m : Month (Number)
# %A : Day of Week (Name)
# %B : Month Name
# %d : Day of Month (Number)