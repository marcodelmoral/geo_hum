import multiprocessing as mp
import os
import time
import re
import geopandas as gpd


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


def procesa_shp(archivo):
    start_time = time.time()
    import django
    django.setup()
    from humanitaria.models import Servicio, Manzana
    map_fix = {
        "Área Verde": "Áreas Verdes",
        "Estación de Transporte Forán*": "Estación de Transporte Foráneo",
        "Observataorio Astronómico": "Observatorio Astronómico",
    }
    map_servicio = dict((y, x) for x, y in Servicio.SERVICIO_TIPO)
    map_condicion = dict((y, x) for x, y in Servicio.CONDICION_TIPO)
    map_geografico = dict((y, x) for x, y in Servicio.GEOGRAFICO_TIPO)
    map_ambito = dict((y, x) for x, y in Servicio.AMBITO_TIPO)
    map_tipo = dict((y, x) for x, y in Manzana.MANZANA_TIPO)
    localidad = [f for f in os.listdir(archivo) if
                 re.search(r'\b\d\d('
                           r'l).shp\b', f)][0]
    manzana = [f for f in os.listdir(archivo) if
               re.search(r'\b\d\d('
                         r'm).shp\b', f)][0]

    dfl = gpd.read_file(os.path.join(archivo, localidad), encoding='latin-1')
    dfl['AMBITO'] = dfl.AMBITO.map(map_ambito).astype('int32')
    salida_localidad = localidad[:-4] + '_procesado.shp'
    dfl.to_file(os.path.join(archivo, salida_localidad))

    dfm = gpd.read_file(os.path.join(archivo, manzana), encoding='latin-1')
    dfm['AMBITO'] = dfm.AMBITO.map(map_ambito).astype('int32')
    dfm['TIPOMZA'] = dfm.TIPOMZA.map(map_tipo).astype('int32')
    salida_manzana = manzana[:-4] + '_procesado.shp'
    dfm.to_file(os.path.join(archivo, salida_manzana))

    sia_file = [ele for ele in
                os.listdir(archivo) if 'sia.shp' in ele][0]
    sip_file = [ele for ele in
                os.listdir(archivo) if 'sip.shp' in ele][0]
    dfa = gpd.read_file(os.path.join(archivo, sia_file),
                        codec='latin-1')
    dfp = gpd.read_file(os.path.join(archivo, sip_file),
                        codec='latin-1')
    num_estado = sia_file[:2]
    dfa['AREA'] = dfa['geometry'].astype(str)
    dfa['geometry'] = dfa['geometry'].centroid
    dfp['AREA'] = None
    df = dfp.append(dfa, sort=True)
    df['TIPO'] = df.TIPO.replace(map_fix)
    df['TIPO'] = df.TIPO.map(map_servicio).astype('int32')
    df['CONDICION'] = df.CONDICION.map(map_condicion).astype('int32')
    df['GEOGRAFICO'] = df.GEOGRAFICO.map(map_geografico).astype('int32')
    df['AMBITO'] = df.AMBITO.map(map_ambito).astype('int32')
    df.to_file(os.path.join(archivo, f'{num_estado}serv.shp'))
    final = time.time() - start_time
    return archivo, final


def paralelo_preprocesa_shp(carpeta):
    start_time = time.time()
    print(f"Inicio : {time.ctime()}\n")
    n = mp.cpu_count()
    print(f"Número de procesadores: {n}\n")
    pool = mp.Pool(n)
    estados = obtener_estados(carpeta)
    results = [pool.apply_async(procesa_shp, args=(i,)) for i in estados]

    pool.close()

    for ele in results:
        s = ele.get()
        print(f'Archivo: {s[0]}\nFinalizado en: {s[1]} segundos\n')
    print(f"Final: {time.ctime()}\n")
    final = time.time() - start_time
    print(f'Procesamiento en paralelo terminado en: {final} segundos')


def secuencial_preprocesa_shp(carpeta):
    start_time = time.time()
    print(f"Inicio : {time.ctime()}\n")
    estados = obtener_estados(carpeta)
    results = [procesa_shp(i) for i in estados]
    print(f"Final: {time.ctime()}\n")
    print(results)
    final = time.time() - start_time
    print(f'Procesamiento secuencial terminado en: {final} segundos')


def preprocesa_shp(carpeta, paralelo=True):
    if paralelo:
        paralelo_preprocesa_shp(carpeta)
    else:
        secuencial_preprocesa_shp(carpeta)


if __name__ == "__main__":
    folder = 'data/889463674658_s'
    preprocesa_shp(folder)
