import math
import os

import pandas as pd

from humanitaria.models import Entidad


def procesa_totales(diccionario):
    for key, value in diccionario.items():
        if type(value) == str:
            diccionario[key] = int(value)
        elif math.isnan(value):
            diccionario[key] = None

    return diccionario


archivo_test = 'RESAGEBURB_30XLS10.xls'
test = ['POBTOT', 'POBMAS', 'POBFEM', 'P_0A2', 'P_0A2_M', 'P_0A2_F']
folder = 'C:\\Users\\marco\\PycharmProjects\\geo_hum\\data\\poblacionales'

for subdir, dirs, files in os.walk(folder):
    for file in files:
        if 'xls' in file:
            df = pd.read_excel(os.path.join(folder, file), dtype={'ENTIDAD':
                                                                  str,
                                                                  'MUN': str,
                                                                  'LOC': str,
                                                                  'AGEB': str,
                                                                  'MZA': str})

            entidad = Entidad.objects.get(nomgeo=df['NOM_ENT'][0])
            df_entidad_totales = df.loc[df['NOM_LOC'] == 'Total de la entidad']
            totales_entidad = df_entidad_totales[test].to_dict('records')
            entidad.update(**procesa_totales(totales_entidad))

            df_municipio_totales = df.loc[df['NOM_LOC'] == 'Total del ' 
                                                           'municipio']
            for i, row in df_municipio_totales.iterrows():
                municipio = entidad.municipio_set.get(cve_mun=str(row['MUN']))
                totales_municipio = row[test].to_dict()
                municipio.update(**procesa_totales(totales_municipio))

            df_localidades_totales = df.loc[df['NOM_LOC'] == 'Total de la ' 
                                                             'localidad urbana']
            for i, row in df_localidades_totales.iterrows():
                municipio = entidad.municipio_set.get(cve_mun=str(row['MUN']))
                localidad = municipio.localidad_set.get(cve_loc=str(row['LOC']))
                totales_localidad = row[test].to_dict()
                localidad.update(**procesa_totales(totales_localidad))

            df_agebu_totales = df.loc[df['NOM_LOC'] == 'Total AGEB urbana']
            for i, row in df_agebu_totales.iterrows():
                municipio = entidad.municipio_set.get(cve_mun=str(row['MUN']))
                localidad = municipio.localidad_set.get(cve_loc=str(row['LOC']))
                agebu = localidad.agebu_set.get(cve_ageb=str(row['AGEB']))
                totales_agebu = row[test].to_dict()
                agebu.update(**procesa_totales(totales_agebu))

            df_manzanas_totales = df[~df['NOM_LOC'].str.match('Total')]
            for i, row in df_manzanas_totales.iterrows():
                municipio = entidad.municipio_set.get(cve_mun=str(row['MUN']))
                localidad = municipio.localidad_set.get(cve_loc=str(row['LOC']))
                ageb = localidad.agebu_set.get(cve_ageb=str(row['AGEB']))
                manzana = ageb.manzana_set.get(cve_mza=str(row['MZA']))
                totales_manzana = row[test].to_dict()
                manzana.update(**procesa_totales(totales_manzana))




