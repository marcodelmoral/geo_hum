import os
import re

import geopandas as gpd
import unidecode


def ambito(entrada):
    entrada = unidecode.unidecode(entrada.lower())
    if entrada == 'urbana':
        return 1
    elif entrada == 'rural':
        return 2
    else:
        return 0


def tipomza(entrada):
    entrada = unidecode.unidecode(entrada.lower())
    if entrada == 'tipica':
        return 1
    elif entrada == 'atipica':
        return 2
    elif entrada == 'contenedora':
        return 3
    elif entrada == 'contenida':
        return 4
    elif entrada == 'economica':
        return 5
    elif 'edificio' in entrada:
        return 6
    elif entrada == 'glorieta':
        return 7
    elif 'parque' in entrada:
        return 8
    elif entrada == 'camellon':
        return 9
    else:
        return 0


# Aqui use el WLS
folder = '/mnt/c/Users/marco/PycharmProjects/geo_hum/data/889463674658_s'
print(folder)
for subdir, dirs, files in os.walk(folder):
    localidad = [f for f in os.listdir(subdir) if re.search(r'\b\d\d(l).shp\b', f)]
    manzana = [f for f in os.listdir(subdir) if re.search(r'\b\d\d(m).shp\b', f)]

    for e in localidad:
        print(os.path.join(subdir, e))
        df = gpd.read_file(os.path.join(subdir, e), encoding='latin-1')
        df['AMBITO'] = df.AMBITO.apply(ambito)
        salida = e[:-4] + '_procesado.shp'
        print(salida)
        df.to_file(os.path.join(subdir, salida))
    for e in manzana:
        print(os.path.join(subdir, e))
        df = gpd.read_file(os.path.join(subdir, e), encoding='latin-1')
        df['AMBITO'] = df.AMBITO.apply(ambito)
        df['TIPOMZA'] = df.TIPOMZA.apply(tipomza)
        salida = e[:-4] + '_procesado.shp'
        print(salida)
        df.to_file(os.path.join(subdir, salida))


