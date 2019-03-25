import os

import math
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


def run_infraestructura():
    for subdir, dirs, files in os.walk(folder):
        for file in files:
            if 'DBF' in file:
                dbf = Dbf5(os.path.join(folder, file), codec='latin-1')
                df = dbf.to_dataframe()
                df.columns = [procesa_columnas(col) for col in df.columns]
                columnas = list(df.columns)[8:-1]
                for i, row in df.iterrows():
                    entidad = Entidad.objects.get(cve_ent=str(row['ENT']))
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
                        print(str(manzana))
                        totales_manzana = row[columnas].to_dict()
                        manzana.update(**procesa_totales(totales_manzana))
                    except:
                        pass


if __name__ == "__main__":
    run_infraestructura()


