import requests
import xml.etree.ElementTree as ET
import pandas 
import gspread
from gspread_dataframe import set_with_dataframe
from indices import indices

paises = ['USA', 'NZL', 'CAN', "AUS", 'GBR']
lista = list()
for pais in paises:
    response = requests.get(f'http://tarea-4.2021-1.tallerdeintegracion.cl/gho_{pais}.xml')
    root = ET.fromstring(response.content)

    # Sacar indices relevantes 
    # lala = root.findall('Fact')
    # for _ in lala:
    #     indices_gho.add(_.find('GHO').text)
    # for indice in indices_gho:
    #     print(indice)
    #     print()
    # break
    columnas = [
        "YEAR",
        "GHO",
        "COUNTRY",
        "GHECAUSES",
        "SEX",
        "AGEGROUP",
        "Display",
        "High",
        "Low",
        "Numeric"
    ]

    for node in root: 
        info = dict()
        for data in columnas:
            if node.find('GHO').text in indices: 
                if node.find(data) is not None: 
                    variable = node.find(data).text
                    if data == 'Numeric':
                        variable = float(variable)
                else: 
                    variable = None
                info[data] = variable
        if info:
            lista.append(info)


tabla = pandas.DataFrame(lista, columns = columnas)

gc=gspread.service_account(filename='credentials.json')
sh = gc.open_by_key('10GK0rtJUayD4JsWhR4jsq2of-8QkzaVfpc5AJxkuSi8')
worksheet = sh.get_worksheet(0)
worksheet.clear()
set_with_dataframe(worksheet, tabla)


