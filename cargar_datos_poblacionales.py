import os

import math
import numpy as np
import pandas as pd

from humanitaria.models import Entidad


def procesa_totales(diccionario):
    for key, value in diccionario.items():
        if type(value) == str:
            try:
                diccionario[key] = int(value)
            except:
                diccionario[key] = None
        elif math.isnan(value):
            diccionario[key] = None

    return diccionario


folder = 'C:\\Users\\marco\\PycharmProjects\\geo_hum\\data\\poblacionales'


def run_poblacionales():
    for subdir, dirs, files in os.walk(folder):
        for file in files[14:]:
            if file.endswith('.xls'):
                archivo = os.path.join(folder, file)
                print(archivo)
                dfs = pd.read_excel(archivo,
                                    dtype={
                                       'ENTIDAD': str,
                                       'MUN': str,
                                       'LOC': str,
                                       'AGEB': str,
                                       'MZA': str
                                    },
                                    sheet_name=None)
                # Combina todos las hojas del excel en un solo dataframe
                df = pd.DataFrame()
                for _, ele in dfs.items():
                    if df.empty:
                        df = ele
                    else:
                        df.append(ele)
                df = df.replace('*', np.nan)
                entidad = Entidad.objects.filter(cve_ent=df['ENTIDAD'][0])
                df_entidad_totales = df[df['NOM_LOC'].str.contains('total de la '
                                                                   'entidad',
                                                                   regex=False,
                                                                   case=False,
                                                                   na=False)]
                totales_entidad = df_entidad_totales.to_dict('records')
                entidad.update(**procesa_totales(totales_entidad[0]))

                df_municipio_totales = df[df['NOM_LOC'].str.contains('total del '
                                                                     'municipio',
                                                                     regex=False,
                                                                     case=False,
                                                                     na=False)]
                for i, row in df_municipio_totales.iterrows():
                    entidad = Entidad.objects.get(cve_ent=df['ENTIDAD'][0])
                    municipio = entidad.municipio_set.filter(cve_mun=str(row[
                                                                             'MUN'])
                                                             )
                    totales_municipio = row.to_dict()
                    municipio.update(**procesa_totales(totales_municipio))

                df_localidades_totales = df[df['NOM_LOC'].str.contains('total de '
                                                                       'la '
                                                                       'localidad '
                                                                       'urbana',
                                                                       regex=False,
                                                                       case=False,
                                                                       na=False)]
                for i, row in df_localidades_totales.iterrows():
                    entidad = Entidad.objects.get(cve_ent=df['ENTIDAD'][0])
                    municipio = entidad.municipio_set.get(cve_mun=str(row['MUN']))
                    localidad = municipio.localidad_set.filter(cve_loc=str(row[
                                                                             'LOC'])
                                                               )
                    totales_localidad = row.to_dict()
                    localidad.update(**procesa_totales(totales_localidad))

                df_agebu_totales = df[df['NOM_LOC'].str.contains('total ageb '
                                                                 'urbana',
                                                                 regex=False,
                                                                 case=False,
                                                                 na=False)]
                for i, row in df_agebu_totales.iterrows():
                    entidad = Entidad.objects.get(cve_ent=df['ENTIDAD'][0])
                    municipio = entidad.municipio_set.get(cve_mun=str(row['MUN']))
                    # No existe San Jose Vieno en BJS 2047
                    try:
                        localidad = municipio.localidad_set.get(cve_loc=str(
                            row['LOC']))
                        agebu = localidad.agebu_set.filter(cve_ageb=str(
                            row['AGEB']))
                        totales_agebu = row.to_dict()
                        agebu.update(**procesa_totales(totales_agebu))
                    except:
                        pass

                df_manzanas_totales = df[~df['NOM_LOC'].str.contains('total',
                                                                     regex=False,
                                                                     case=False,
                                                                     na=False)]
                for i, row in df_manzanas_totales.iterrows():
                    entidad = Entidad.objects.get(cve_ent=df['ENTIDAD'][0])
                    municipio = entidad.municipio_set.get(cve_mun=str(row['MUN']))
                    try:
                        localidad = municipio.localidad_set.get(cve_loc=str(
                            row['LOC']))
                        # En aguascalientes no hay ageb 1301 para mun 01 loc 001
                        try:
                            ageb = localidad.agebu_set.get(cve_ageb=str(
                                row['AGEB']))
                        except:
                            try:
                                ageb = municipio.agebr_set.get(cve_ageb=str(
                                    row['AGEB']))
                            except:
                                pass
                        manzana = ageb.manzana_set.filter(cve_mza=str(row['MZA']))
                        totales_manzana = row.to_dict()
                        manzana.update(**procesa_totales(totales_manzana))
                    except:
                        pass

if __name__ == "__main__":
    run_poblacionales()


