import multiprocessing as mp
import os
import re
import time
from django.contrib.gis.utils import LayerMapping


def obtener_estados(carpeta):
    estados = []
    for estado in os.listdir(carpeta):
        if 'zip' not in estado:
            estado_folder = os.path.join(carpeta, estado)
            for datos in os.listdir(estado_folder):
                if 'conjunto de datos' in datos:
                    datos_folder = os.path.join(estado_folder, datos)
                    estados.append(datos_folder)
    return estados


def cargar_shp(archivo):
    start_time = time.time()
    import django
    django.setup()
    from humanitaria.models import Entidad, Municipio, Localidad, Agebu, Agebr, \
        Manzana, \
        entidad_mapping, municipio_mapping, localidad_mapping, agebu_mapping, \
        manzana_mapping, agebr_mapping

    entidad = [f for f in os.listdir(archivo) if
               re.search(r'\b\d\d(ent).shp\b', f)][0]
    municipio = [f for f in os.listdir(archivo) if
                 re.search(r'\b\d\d(mun).shp\b', f)][0]
    agebu = [f for f in os.listdir(archivo) if
             re.search(r'\b\d\d('
                       r'a).shp\b', f)][0]
    agebr = [f for f in os.listdir(archivo) if
             re.search(r'\b\d\d('
                       r'ar).shp\b', f)][0]
    localidad = [f for f in os.listdir(archivo) if
                 re.search(r'\b\d\d('
                           r'l_procesado).shp\b', f)][0]
    manzana = [f for f in os.listdir(archivo) if
               re.search(r'\b\d\d('
                         r'm_procesado).shp\b', f)][0]

    lme = LayerMapping(Entidad, os.path.join(archivo, entidad),
                       entidad_mapping,
                       transform=True, encoding='latin-1')
    lme.save(strict=True, verbose=True)

    lme = LayerMapping(Municipio, os.path.join(archivo, municipio),
                       municipio_mapping,
                       transform=True, encoding='latin-1')
    lme.save(strict=True, verbose=True)

    lme = LayerMapping(Localidad, os.path.join(archivo, localidad),
                       localidad_mapping,
                       transform=True, encoding='latin-1')
    lme.save(strict=True, verbose=True)

    lme = LayerMapping(Agebu, os.path.join(archivo, agebu),
                       agebu_mapping,
                       transform=True, encoding='latin-1')
    lme.save(strict=True, verbose=True)

    lme = LayerMapping(Agebr, os.path.join(archivo, agebr),
                       agebr_mapping,
                       transform=True, encoding='latin-1')
    lme.save(strict=True, verbose=True)

    lme = LayerMapping(Manzana, os.path.join(archivo, manzana),
                       manzana_mapping,
                       transform=True, encoding='latin-1')
    lme.save(strict=True, verbose=True)

    final = time.time() - start_time
    return archivo, final


def paralelo_carga_shp(carpeta):
    start_time = time.time()
    print(f"Inicio : {time.ctime()}\n")
    n = mp.cpu_count()
    print(f"Número de procesadores: {n}\n")
    pool = mp.Pool(n)
    estados = obtener_estados(carpeta)
    results = [pool.apply_async(cargar_shp, args=(i,)) for i in
               estados]
    pool.close()
    for ele in results:
        s = ele.get()
        print(f'Archivo: {s[0]}\nFinalizado en: {s[1]} segundos\n')
    print(f"Final: {time.ctime()}\n")
    final = time.time() - start_time
    print(f'Procesamiento en paralelo terminado en: {final} segundos')


def secuencial_carga_shp(carpeta):
    start_time = time.time()
    print(f"Inicio : {time.ctime()}\n")
    estados = obtener_estados(carpeta)
    results = [cargar_shp(i) for i in estados]
    print(f"Final: {time.ctime()}\n")
    print(results)
    final = time.time() - start_time
    print(f'Procesamiento secuencial terminado en: {final} segundos')


def carga_shp(carpeta, paralelo=True):
    if paralelo:
        paralelo_carga_shp(carpeta)
    else:
        secuencial_carga_shp(carpeta)


if __name__ == "__main__":
    folder = 'data/889463674658_s'
    carga_shp(folder)
