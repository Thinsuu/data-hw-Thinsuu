from collections import defaultdict
import csv
from datetime import datetime, timedelta
from os import name
from pprint import pprint
from typing import Counter
from collections import defaultdict
from matplotlib import container
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from numpy.lib.arraysetops import unique # for random data
import pandas as pd  # for convinience


filename = '/Users/thinsu/Documents/coding/Wastewater Project/SLU_wastewater_data(1).csv'
# 7)	Draw the timeline of COVID 19 variants found in wastewater between 2021-2023 by region.
def task07():
    variants_week_level = {
        'SARS-CoV2/PMMoV x 1000': defaultdict(int),
        'infA/PMMoV x 1000': defaultdict(int),
        'infB/PMMoV x 1000': defaultdict(int),
    }
    with open(filename, "r", encoding="utf-8", errors="ignore") as csvfile:
        reader = csv.DictReader(csvfile, delimiter= ',', quotechar='|')
        
        for row in reader:
            if "*" in row['week']:
                continue  # skip this line and go right to the next one.

            week_value = row['week']
            date_obj = datetime.strptime(week_value + '.1', '%Y-%W.%w')
            if date_obj < datetime(2023, 1, 1):
                continue

            for column_name, value in row.items():
                if column_name in variants_week_level.keys():
                    try:
                        covid_level = float(value)
                    except ValueError:
                        continue
                    variants_week_level[column_name][date_obj] += covid_level

    fig, ax = plt.subplots(figsize= (16,9))
    for variant_name, week_level in variants_week_level.items():
        ax.plot(
            week_level.keys(),
            week_level.values(),
            linewidth=0.5,
            linestyle='solid',
            label=variant_name,
        )
    ax.set_title(f'Level of COVID in Regions')
    ax.set_yscale('log')
    plt.xticks(rotation = 45, size = 4)
    # plt.show()
    plt.savefig('/Users/thinsu/Documents/coding/Wastewater Project/COVID 19 Variants found in Wastewater Between 2021-2023.png')
    plt.close()

task07()



# 1)	How many Corona cases around the world by continents yearly from 2021-2023: Oceania, Africa, North-, South-America, Europe, Asia.
worldfile = '/Users/thinsu/Documents/coding/Wastewater Project/owid-wholeworld_covid-data_231206.csv'
def task01():
    with open(worldfile, "r", encoding="utf-8", errors="ignore") as csvf:
        reader_wf = csv.DictReader(csvf, delimiter= ';', quotechar='|')
        data = list(reader_wf)
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'], errors='coerce') 
    df['total_cases'] = pd.to_numeric(df['total_cases'], errors='coerce')

    start_date = '2021-01-01'
    end_date = '2023-12-31'
    df_filtered = df[(df['date'] >= start_date) & (df['date'] <= end_date) & (df['continent'] != '')]
    
    continent_cases = df_filtered.groupby('continent')['total_cases'].sum()

    fig, ax = plt.subplots(figsize=(10, 6))
    continent_cases.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_title('Total COVID-19 Cases by Continent (2021-2023)')
    ax.set_xlabel('Continent')
    ax.set_ylabel('Total Cases (millions)')
    plt.xticks(rotation=45, ha='right')
    plt.savefig('/Users/thinsu/Documents/coding/Wastewater Project/COVID levels by Continent 2021-2023.png')
    plt.close()
    
# task01()

# 2)	Depict the Corona cases with live timeline by continent from 2020-2023.
def task02():
    with open(worldfile, "r", encoding="utf-8", errors="ignore") as csvf:
        reader_wf = csv.DictReader(csvf, delimiter= ';', quotechar='|')
        data = list(reader_wf)
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['total_cases'] = pd.to_numeric(df['total_cases'], errors='coerce')

    start_date = '2020-01-01'
    end_date = '2023-12-31'
    df_filtered = df[(df['date'] >= start_date) & (df['date'] <= end_date) & (df['continent'] != '')]
    
    continent_cases_line = df_filtered.groupby(['continent', 'date'])['total_cases'].sum().reset_index()

    fig = px.line(
        continent_cases_line,
        x='date',
        y='total_cases',
        color='continent',
        title='COVID 19 Cases by Continent (2020-2023)',
        labels={'date': 'Date', 'total_cases': 'Total Cases', 'continent': 'Continent'},
        range_x=[start_date, end_date],
    )
    fig.update_layout(legend=dict(x=1.02, y=0.5))
    fig.update_traces(hovertemplate='%{x|%Y-%m-%d}')

    # if fig.layout.updatemenus and fig.layout.updatemenus[0].buttons:
        # fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 1000
        # fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 500
        # fig.layout.updatemenus[0].buttons[0].args[1]['fromcurrent'] = True
        # fig.layout.updatemenus[0].buttons[0].args[1]['easing'] = 'linear'
    fig.show()
    fig.close()

# task02()
# # http://127.0.0.1:58782 plot link for task 02


# 3)	Which of 3 continents have the highest corona cases in 2023? Show by monthly trend.
def task03():
    worldfile = '/Users/thinsu/Documents/coding/Wastewater Project/owid-wholeworld_covid-data_231206.csv'
    with open(worldfile, "r", encoding="utf-8", errors="ignore") as csvf:
        reader_wf = csv.DictReader(csvf, delimiter=';', quotechar='|')

        continent_cases = defaultdict(int)
        all_data = list(reader_wf)

        for row in all_data:
            if row['continent'] != '' and row['total_cases'] != '':
                continent_cases[row['continent']] += int(row['total_cases'])

        top_continents = sorted(continent_cases.items(), key=lambda x: x[1], reverse=True)[:3]
    
        top_continent_monthly_cases = defaultdict(list)
        for row in all_data:
            for continent, _ in top_continents:
                if row['continent'] == continent and row['date'] != '' and row['total_cases'] != '':
                    week_value = row['date']
                    date_obj = datetime.strptime(week_value, '%Y-%m-%d')
                    if date_obj > datetime(2023, 5, 1):
                        continue
                    
                    if row['continent'] not in top_continent_monthly_cases.keys():
                        top_continent_monthly_cases[row['continent']] = {}
                    top_continent_monthly_cases[continent][date_obj] = int(row['total_cases'])

    plt.figure(figsize=(10, 6))

    for continent, cases in top_continent_monthly_cases.items():
        cases = dict(sorted(cases.items()))
        plt.plot(cases.keys(), cases.values(), label=continent)

    plt.title('Monthly Trend of COVID-19 Cases in 2023 (Top 3 Continents)')
    plt.xlabel('Month')
    plt.ylabel('Total Cases')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid(True)
    plt.savefig('/Users/thinsu/Documents/coding/Wastewater Project/Highest Top 3 continents in 2023.png')
    plt.close()
# task03()

# 4)	Which 5 countries have the highest corona cases found in 2023?
def task04():
    worldfile = '/Users/thinsu/Documents/coding/Wastewater Project/owid-wholeworld_covid-data_231206.csv'
    with open(worldfile, "r", encoding="utf-8", errors="ignore") as csvf:
        reader_wf = csv.DictReader(csvf, delimiter=';', quotechar='|')

        country_cases = defaultdict(int)

        for row in reader_wf:
            if row['location'] and row['continent'] and row['new_cases'] and row['date'].startswith('2023'):  
                country_cases[row['location']] += int(row['new_cases'])
        
    top_countries = sorted(country_cases.items(), key=lambda x: x[1], reverse=True)[:5]
    countries, cases = zip(*top_countries)
    plt.figure(figsize=(10, 6))
    plt.bar(countries, cases, color='skyblue')
    plt.title('Top 5 Countries with the Highest COVID-19 Cases in 2023')
    plt.xlabel('Countries')
    plt.ylabel('Total Cases in Millions')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('/Users/thinsu/Documents/coding/Wastewater Project/Top 5 countries regarding Corona cases in 2023.png')
    plt.close()

    # print('Top 5 countries with the highest COVID 19 cases in 2023')
    # for country, cases in top_countries:
    #     print(f"{country}: {cases} cases")

# task04()

# 5)	Compare the EU and USA corona cases between 2021-2023.
def get_days_since_beginning(date_string):
    start_date = datetime.strptime('2021-01-01', '%Y-%m-%d')
    current_date = datetime.strptime(date_string, '%Y-%m-%d')
    days_since_start = (current_date - start_date).days
    return days_since_start

def task05():
    worldfile = '/Users/thinsu/Documents/coding/Wastewater Project/owid-wholeworld_covid-data_231206.csv'
    with open(worldfile, "r", encoding="utf-8", errors="ignore") as csvf:
        reader_wf = csv.DictReader(csvf, delimiter=';', quotechar='|')

        eu_cases = defaultdict(int)
        usa_cases = defaultdict(int)

        for row in reader_wf:
            date_obj = datetime.strptime(row['date'], '%Y-%m-%d')
            if date_obj < datetime(2021, 1, 1) or date_obj > datetime(2022, 12, 31):
                continue
            if not row['new_cases_smoothed'].isdigit():
                continue
            if row['location'] == 'United States':
                usa_cases[date_obj] += int(row['new_cases_smoothed'])
            elif row['continent'] == 'Europe':
                eu_cases[date_obj] += int(row['new_cases_smoothed'])

        usa_cases = dict(sorted(usa_cases.items()))
        eu_cases = dict(sorted(eu_cases.items()))

        plt.plot(usa_cases.keys(), usa_cases.values(), label='USA')
        plt.plot(eu_cases.keys(), eu_cases.values(), label='EU')

        plt.title('Comparison of Corona Cases in USA and EU (2021-2023)')
        plt.xlabel('Days since 2021-01-01')
        plt.ylabel('Total Cases')
        plt.legend()
        plt.grid(True)
        plt.savefig('/Users/thinsu/Documents/coding/Wastewater Project/Comparison Corona Cases between EU and USA 2021-2023.png')
        plt.close()

# task05()

# 6)	Showcase the monthly data trend between SARS/ CoV 2 variant found at wastewater and number of corona cases in Sweden in 2023?
filename = '/Users/thinsu/Documents/coding/Wastewater Project/SLU_wastewater_data(1).csv'
def task06():
    with open(filename, "r", encoding="utf-8", errors="ignore") as csvfile:
        reader = csv.DictReader(csvfile, delimiter= ',', quotechar='|')

        week_levels = {}
        for line in reader:
            if "*" in line['week']:
                continue  # skip this line and go right to the next one.
                        
            try:
                covid_value = float(line['SARS-CoV2/PMMoV x 1000'])
            except ValueError:
                covid_value = 0.0
            week_value = line['week']
            date_obj = datetime.strptime(week_value + '.1', '%Y-%W.%w')
            if date_obj > datetime(2023, 5, 1):
                continue
            if date_obj not in week_levels.keys():
                week_levels[date_obj] = []
            week_levels[date_obj].append(covid_value)

            average_week = {
                week: sum(covid_level_list)/ len(covid_level_list)
                for week, covid_level_list in week_levels.items()
            }
        # print(average_week)

    onlySweden_file = '/Users/thinsu/Documents/coding/Wastewater Project/owid-covid-data_only_sweden.csv'
    with open(onlySweden_file, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f, delimiter= ';', quotechar='|')
        date_with_newCases = {}
        for title in reader:
            year_week = title['date']
            try:
                new_cases = int(title['new_cases'])
            except ValueError:
                new_cases = 0.0
            year_week = title['date']
            date_obj = datetime.strptime(year_week,'%Y-%m-%d')
            year_week_format = date_obj - timedelta(days=date_obj.weekday() % 7)

            if year_week_format > datetime(2023, 5, 1):
                continue

            if year_week_format not in date_with_newCases:
                date_with_newCases[year_week_format] = 0
            else:
                date_with_newCases[year_week_format] += new_cases    

    plt.plot(
        average_week.keys(),
        average_week.values(),
        linewidth=0.5,
        linestyle='solid',
        color='red',
        # label=channel,
    )
    
    plt.ylim([0, None])
    plt.legend(
        bbox_to_anchor=(1, 0.5),
        loc="center left",
        prop={'size': 8},
        ncol=2,
    )
    plt.axvline(datetime(2022, 5, 1), label='')
    plt.subplots_adjust(right=0.85)
    plt.xticks(rotation=30)
    plt.xlabel('Week')
    plt.ylabel('COVID Level')
    plt.title('COVID Wastewater Level and New Cases by Weekly in Sweden')

    ax = plt.twinx()
    ax.bar(
        date_with_newCases.keys(),
        date_with_newCases.values(),
    )
    plt.ylim([0, max(date_with_newCases.values())])
    plt.savefig('/Users/thinsu/Documents/coding/Wastewater Project/COVID levels by weekly.png')
    plt.close()

# task6()

# 8)	Which seasons has the highest COVID month during 2021-2023 in Sweden?
def task08():
    onlySweden_file = '/Users/thinsu/Documents/coding/Wastewater Project/owid-covid-data_only_sweden.csv'

    df = pd.read_csv(onlySweden_file, delimiter=";")

    df['date'] = pd.to_datetime(df['date'])

    df_2021_2023 = df[(df['date'] >= '2021-01-01') & (df['date'] <= '2023-12-31')]
    
    monthly_sum = df_2021_2023.groupby(df_2021_2023['date'].dt.to_period("M"))['new_cases'].sum()

    highest_month = monthly_sum.idxmax()
    highest_month_data = df_2021_2023[df_2021_2023['date'].dt.to_period("M") == highest_month]

    plt.figure(figsize=(10, 6))
    plt.plot(highest_month_data['date'], highest_month_data['new_cases'], marker='o', linestyle='-', color='b')
    plt.title(f'Highest COVID Month in Sweden: {highest_month}')
    plt.xlabel('Date')
    plt.xticks(rotation=30)
    plt.ylabel('New Cases')
    plt.grid(True)
    plt.savefig('/Users/thinsu/Documents/coding/Wastewater Project/Highest COVID month in Sweden (2021-2023).png')
    plt.close()
# task08()


# 9)	Depict the situation of COVID cases in Nordic countries in 2023.
def task09(data_file):
    data_file = '/Users/thinsu/Documents/coding/Wastewater Project/owid-wholeworld_covid-data_231206.csv'

    df = pd.read_csv(data_file, delimiter=";")

    df['date'] = pd.to_datetime(df['date'])

    nordic_countries = ['Sweden', 'Norway', 'Denmark', 'Finland', 'Iceland']
    df_nordic = df[df['location'].isin(nordic_countries)]

    df_2023 = df_nordic[(df_nordic['date'] >= '2023-01-01') & (df_nordic['date'] <= '2023-12-31')]

    plt.figure(figsize=(12, 8))

    for country in nordic_countries:
        country_data = df_2023[df_2023['location'] == country]
        plt.plot(country_data['date'], country_data['new_cases'], label=country)

    plt.title('COVID Cases in Nordic Countries in 2023')
    plt.xlabel('Date')
    plt.ylabel('New Cases')
    plt.legend()
    plt.grid(True)
    plt.savefig('/Users/thinsu/Documents/coding/Wastewater Project/Situation in Nordic Countries in 2023.png')
    plt.close()
data_file_path = '/Users/thinsu/Documents/coding/Wastewater Project/owid-wholeworld_covid-data_231206.csv'
# task09(data_file_path)

# 10) Show the death rate of COVID in Nordic Countries in 2023.
def task10():
    data_file = '/Users/thinsu/Documents/coding/Wastewater Project/owid-wholeworld_covid-data_231206.csv'

    df = pd.read_csv(data_file, delimiter=";")

    df['date'] = pd.to_datetime(df['date'])

    nordic_countries = ['Sweden', 'Norway', 'Denmark', 'Finland', 'Iceland']
    df_nordic = df[df['location'].isin(nordic_countries)]

    df_2023 = df_nordic[(df_nordic['date'] >= '2023-01-01') & (df_nordic['date'] <= '2023-12-31')]

    plt.figure(figsize=(12, 8))

    for country in nordic_countries:
        country_data = df_2023[df_2023['location'] == country]
        plt.plot(country_data['date'], country_data['new_deaths_smoothed'], label=country)
    plt.title('COVID Death Cases in Nordic Countries in 2023')
    plt.xlabel('Date')
    plt.ylabel('Death Cases')
    plt.legend()
    plt.grid(True)
    plt.savefig('/Users/thinsu/Documents/coding/Wastewater Project/COVID Death Cases in 2023.png')
    plt.close()

task10()
