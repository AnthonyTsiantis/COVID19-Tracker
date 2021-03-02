from flask import redirect, render_template, request, session
from functools import wraps
from bs4 import BeautifulSoup
import requests

def login_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        else:
            return f(*args, **kwargs)
    return function

def global_case():
    source = requests.get("https://www.worldometers.info/coronavirus/").text
    soup = BeautifulSoup(source, 'lxml')
    numbers = []
    for case in soup.find_all('div', class_="maincounter-number"):
        case = case.span.text
        numbers.append(case)

    return numbers

def local_case(state, country):
    source = requests.get("https://www.worldometers.info/coronavirus/").text
    soup = BeautifulSoup(source, 'lxml')
    table = soup.find("table", attrs={"id" : "main_table_countries_today"})
    table_rows = table.find_all("tr")
    d = []
    data = []
    for tr in table_rows:
        td = tr.find_all("td")
        row = [i.text for i in td]
        d.append(row)
    counter = 0
    for row in d:
        data.append([])
        for string in row:
            if string != '' and string != "\n" and string != " " and string != "All":
                data[counter].append(string)
        counter = counter + 1
    data.pop(0)

    c_total = None
    c_deaths = None
    c_recovered = None
    c_rank = None
    country_data ={}

    if country == "United States":
        for row in data:
            if row[1] == "USA":
                c_rank = row[0]
                country_data["c_rank"] = c_rank
                c_total = row[2]
                country_data["c_total"] = c_total
                c_deaths = row[4]
                country_data["c_deaths"] = c_deaths
                c_recovered = row[6]
                country_data["c_recovered"] = c_recovered

                source = requests.get("https://www.worldometers.info/coronavirus/country/us/").text
                soup = BeautifulSoup(source, 'lxml')
                table = soup.find("table", attrs={"id" : "usa_table_countries_today"})
                table_rows = table.find_all("tr")
                d = []
                data = []
                for tr in table_rows:
                    td = tr.find_all("td")
                    row = [i.text for i in td]
                    d.append(row)
                counter = 0
                for row in d:
                    data.append([])
                    for string in row:
                        if string != '' and string != "\n" and string != " " and string != "All" and string != "\xa0":
                            data[counter].append(string)
                    counter = counter + 1
                data.pop(0)
                state = "\n" + str(state) + " "
                s_rank = None
                s_total = None
                s_recovered = None
                state_data = {}

                for row in data:
                    if row[1] == state:
                        s_rank = row[0]
                        state_data["s_rank"] = s_rank
                        s_total = row[2]
                        s_total = s_total.replace(" ", '')
                        state_data["s_total"] = s_total
                        s_deaths = row[4]
                        s_deaths = s_deaths.replace("\n", '')
                        s_deaths = s_deaths.replace(" ", '')
                        state_data["s_deaths"] = s_deaths
                        s_recovered = row[6]
                        state_data["s_recovered"] = s_recovered

    elif country == "United Kingdom":
        for row in data:
            if row[1] == "UK":
                c_rank = row[0]
                country_data["c_rank"] = c_rank
                c_total = row[2]
                country_data["c_total"] = c_total
                c_deaths = row[4]
                country_data["c_deaths"] = c_deaths
                c_recovered = row[6]
                country_data["c_recovered"] = c_recovered
        state_data = "No Local Data Recovered"

    else:
        for row in data:
            if row[1] == country:
                c_rank = row[0]
                country_data["c_rank"] = c_rank
                c_total = row[2]
                country_data["c_total"] = c_total
                c_deaths = row[4]
                country_data["c_deaths"] = c_deaths
                c_recovered = row[6]
                country_data["c_recovered"] = c_recovered
        state_data = "No Local Data Recovered"

    return country_data, state_data