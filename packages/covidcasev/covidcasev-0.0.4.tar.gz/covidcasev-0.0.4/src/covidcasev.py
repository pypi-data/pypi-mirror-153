import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objs as go
import plotly.offline as offline
import subprocess as sp
import os
import sys

if os.path.exists('result.png') == True:
    sp.call("rm result.png",shell=True)

else:
    pass

def main():
    # print('国名を入れてください')
    # country = input()
    # country = str(country)

    country = sys.argv[1]

    sp.call('wget https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv', shell=True)
    sp.call('wget https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv', shell=True)

    df_vaccination = pd.read_csv('vaccinations.csv')
    df_owid_covid = pd.read_csv('owid-covid-data.csv')

    df_country_vac = df_vaccination.query('location == @country')
    df_country_vac['total_vaccinations_ffill'] = df_country_vac['total_vaccinations'].fillna(method='ffill')
    df_country_owid = df_owid_covid.query('location == @country')
    df_country_owid['new_cases_abs'] = df_country_owid['new_cases'].abs()

    covid_vaccinations = go.Bar(x=df_country_vac['date'], y=df_country_vac['total_vaccinations_ffill'], name='ワクチン接種回数',  yaxis='y1')
    covid_infected = go.Scatter(x=df_country_owid['date'], y=df_country_owid['new_cases_abs'], mode = 'lines', name='新規感染者数', yaxis='y2')

    layout = go.Layout(title = 'Covid-19のワクチン接種数と感染者数の関係' + '(' + country + ')',
                xaxis = dict(title = '日付'),
                yaxis = dict(title = 'ワクチン接種数', side = 'right', showgrid=False),
                yaxis2 = dict(title = '新規感染者数', side = 'left', overlaying = 'y', showgrid=False))

    fig = go.Figure(data = [covid_vaccinations, covid_infected], layout = layout)

    fig.show()

    # fig.write_image("test.png")

    sp.call("rm vaccinations.csv",shell=True)
    sp.call("rm owid-covid-data.csv",shell=True)

    fig.write_image("result.png")

if __name__ == "__main__":
    main()