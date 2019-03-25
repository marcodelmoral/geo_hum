import os

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


def tipo_servicio(entrada):
    entrada = unidecode.unidecode(entrada.lower())
    if entrada == 'agua':
        return 1
    elif 'alberca' in entrada:
        return 2
    else:
        return 0


SERVICIO_TIPO = (
        ('No Aplica', 0),
        ('Agua', 1),
        ('Alberca Olímpica', 2),
        ('Antena de Microondas de Telefonía', 3),
        ('Antena de Radio', 4),
        ('Antena de Televisión', 5),
        ('Área Deportiva o Recreativa', 6),
        ('Áreas Verdes', 7),
        ('Aserradero', 8),
        ('Autódromo', 9),
        ('Ayudantía', 10),
        ('Balneario', 11),
        ('Bordo', 12),
        ('Caja de Agua', 13),
        ('Camellón', 14),
        ('Campo de Golf', 15),
        ('Cancha', 16),
        ('Central de Autobuses', 17),
        ('Central de Policía', 18),
        ('Centro de Abastos', 19),
        ('Centro de Espectáculos', 20),
        ('Centro de Rehabilitación', 21),
        ('Centro de Salud', 22),
        ('Edificación Cultural', 23),
        ('Estación de Transporte Foráneo', 24),
        ('Estadio', 25),
        ('Estanque', 26),
        ('Gas', 27),
        ('Gasolinera', 28),
        ('Glorieta', 29),
        ('Hipódromo', 30),
        ('Hospital', 31),
        ('Instalación Terrestre de Telecomunicación', 32),
        ('Jardín', 33),
        ('Lago', 34),
        ('Laguna', 35),
        ('Lienzo Charro', 36),
        ('Medio Superior', 37),
        ('Mixto', 38),
        ('Monumento u Obelisco', 39),
        ('Museo', 40),
        ('Observatorio Astronómico', 41),
        ('Palacio Municipal', 42),
        ('Palacio de Gobierno', 43),
        ('Parque', 44),
        ('Petróleo', 45),
        ('Planta Petroquímica', 46),
        ('Planta de Tratamiento de Agua', 47),
        ('Plaza de Toros', 48),
        ('Preescolar', 48),
        ('Presa', 50),
        ('Primaria', 51),
        ('Reclusorio', 52),
        ('Secundaria', 53),
        ('Superior', 54),
        ('Tanque Elevado', 55),
        ('Torre de Microondas', 56),
        ('Unidad Deportiva', 57),
        ('Zoológico', 58)
    )

folder = 'C:/Users/marco/PycharmProjects/geo_hum/data/889463674658_s'

for estado in os.listdir(folder):
    if 'zip' not in estado:
        estado_folder = os.path.join(folder, estado)
        for datos in os.listdir(estado_folder):
            if 'conjunto de datos' in datos:
                datos_folder = os.path.join(estado_folder, datos)
                sia_file = [ele for ele in
                            os.listdir(datos_folder) if 'sia.shp' in ele][0]

                sip_file = [ele for ele in
                            os.listdir(datos_folder) if 'sip.shp' in ele][0]
                num_estado = sia_file[:2]
                dfa = gpd.read_file(os.path.join(datos_folder, sia_file),
                                    codec='latin-1')
                dfp = gpd.read_file(os.path.join(datos_folder, sip_file),
                                    codec='latin-1')

                dfa['geometry'] = dfa['geometry'].centroid

                df = dfp.append(dfa)

                df.to_file(os.path.join(datos_folder, f'{num_estado}serv.shp'))
