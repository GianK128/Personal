# 
# GitHub: @GianK128
#

import os
import requests as r
import datetime as dt

clear = lambda: os.system('cls')
selected_region = "argentina"
region_text = selected_region.replace('-', ' ').capitalize()

GLOBAL, REGION, WEEKLY, CH_REGION, QUIT = range(1, 6)

MAIN_MENU_STR = """
=====COVID-19 STATS=====
  [1]. Resumen Mundial.
  [2]. Resumen de {0}.
  [3]. Resumen Semanal de {0}.
  [4]. Cambiar Región.
  [5]. Salir.
"""

SUMMARY_STR = """
=====RESUMEN {0}=====
Fecha: {1}

Numero de casos nuevos: {2}.
Numero de casos totales: {3}.

Numero de muertes nuevas: {4}.
Numero de muertes total: {5}.

Numero de recuperados nuevos: {6}.
Numero de recuperados total: {7}.
"""

WEEKLY_STR = """
=====RESUMEN SEMANAL DE {0}=====
Desde: {1} 
Hasta: {2}

Nuevos casos confirmados: {3}.

Nuevos muertos confirmados: {4}.

Nuevos casos activos: {5}
"""

def get_global_data():
    data = r.get("https://api.covid19api.com/summary").json()
    summary = data['Global']
    fecha = dt.datetime.strptime(summary['Date'], '%Y-%m-%dT%H:%M:%S.%fZ')
    fecha = fecha.strftime('%d/%m/%Y %H:%M (UTC)')
    print(SUMMARY_STR.format(
        "GLOBAL",
        fecha, 
        summary['NewConfirmed'],
        summary['TotalConfirmed'],
        summary['NewDeaths'],
        summary['TotalDeaths'],
        summary['NewRecovered'],
        summary['TotalRecovered']
    ))
    return input("> Presione ENTER para continuar.")

def get_region_data():
    data = r.get("https://api.covid19api.com/summary").json()
    for country in data['Countries']:
        if country['Slug'] == selected_region:
            fecha = dt.datetime.strptime(country['Date'], '%Y-%m-%dT%H:%M:%S.%fZ')
            fecha = fecha.strftime('%d/%m/%Y %H:%M (UTC)')
            print(SUMMARY_STR.format(
                f"DE {region_text.upper()}",
                fecha, 
                country['NewConfirmed'],
                country['TotalConfirmed'],
                country['NewDeaths'],
                country['TotalDeaths'],
                country['NewRecovered'],
                country['TotalRecovered']
            ))
    return input("> Presione ENTER para continuar.")

def get_weekly_region_data():
    today = dt.datetime.today()
    week_ago = today - dt.timedelta(days=7)
    data = r.get(f"https://api.covid19api.com/country/{selected_region}?from={week_ago.strftime('%Y-%m-%dT00:00:00Z')}&to={today.strftime('%Y-%m-%dT00:00:00Z')}").json()
    confirmed = data[-1]['Confirmed'] - data[0]['Confirmed']
    deaths = data[-1]['Deaths'] - data[0]['Deaths']
    active = data[-1]['Active'] - data[0]['Active']
    print(WEEKLY_STR.format(
        selected_region.upper(),
        week_ago.strftime("%d/%m/%Y %H:%M"),
        today.strftime("%d/%m/%Y %H:%M"),
        confirmed,
        deaths,
        active
    ))
    return input("> Presione ENTER para continuar.")

def change_selected_region():
    global selected_region, region_text
    while True:
        i = input("Ingrese la nueva region:\n")
        if i.isalpha():
            selected_region = i.lower().replace(' ','-')
            region_text = i.lower().capitalize()
            print("Región cambiada.")
            break
        else:
            print("Region invalida (no se detectan solo letras).")
    return input("> Presione ENTER para continuar.")

def prompt_exit():
    while True:
        i = input("¿Quieres salir? [y/n] ")
        if i.strip() == 'y':
            exit(1)
        elif i.strip() == 'n':
            break

choice_executer = {
    GLOBAL: get_global_data,
    REGION: get_region_data,
    WEEKLY: get_weekly_region_data,
    CH_REGION: change_selected_region,
    QUIT: prompt_exit,
}

if __name__ == "__main__":
    while True:
        choice = int(input(MAIN_MENU_STR.format(region_text) + ">> "))
        if choice < 1 or choice > 5:
            print("Eleccion invalida.")
            input()
            continue
        choice_executer[choice]()
        clear()
