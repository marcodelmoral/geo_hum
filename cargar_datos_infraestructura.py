import math
import os

from simpledbf import Dbf5

from humanitaria.models import Entidad


def procesa_totales(diccionario):
    for key, value in diccionario.items():
        if type(value) == str:
            diccionario[key] = int(value)
        elif math.isnan(value):
            diccionario[key] = None

    return diccionario


def procesa_columnas(columna):
    if columna.endswith('_'):
        return columna[:-1]
    else:
        return columna


folder = 'C:\\Users\\marco\\PycharmProjects\\geo_hum\\data\\infraestructura'

for subdir, dirs, files in os.walk(folder):
    for file in files:
        if 'DBF' in file:
            dbf = Dbf5(os.path.join(folder,), codec='latin-1')

            df = dbf.to_dataframe()

            df.columns = [procesa_columnas(col) for col in df.columns]

            for i, row in df.iterrows():
                entidad = Entidad.objects.get(cve_geo=row['ENT'])
                municipio = entidad.municipio_set.get(cve_mun=str(row['MUN']))
                localidad = municipio.localidad_set.get(cve_loc=str(row['LOC']))
                ageb = localidad.agebu_set.get(cve_ageb=str(row['AGEB']))
                manzana = ageb.manzana_set.get(cve_mza=str(row['MZA']))
                totales_manzana_infra = row.to_dict()
                manzana.update(**procesa_totales(totales_manzana_infra))




