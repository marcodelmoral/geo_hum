import os
import re

from django.contrib.gis.utils import LayerMapping

from humanitaria.models import Entidad, Municipio, Localidad, Agebu, Agebr, \
    Manzana, \
    entidad_mapping, municipio_mapping, localidad_mapping, agebu_mapping, \
    manzana_mapping, agebr_mapping


def run(verbose=True):

    folder = 'C:\\Users\\marco\\PycharmProjects\\geo_hum\\data\\889463674658_s'
    print(folder)
    for subdir, dirs, files in os.walk(folder):
        print(subdir)
        entidad = [f for f in os.listdir(subdir) if re.search(r'\b\d\d(ent).shp\b', f)]
        municipio = [f for f in os.listdir(subdir) if re.search(r'\b\d\d(mun).shp\b', f)]
        agebu = [f for f in os.listdir(subdir) if re.search(r'\b\d\d('
                                                            r'a).shp\b', f)]
        agebr = [f for f in os.listdir(subdir) if re.search(r'\b\d\d('
                                                            r'ar).shp\b', f)]
        localidad = [f for f in os.listdir(subdir) if re.search(r'\b\d\d(l).shp\b', f)]
        manzana = [f for f in os.listdir(subdir) if re.search(r'\b\d\d(m).shp\b', f)]
        for e in entidad:
            lme = LayerMapping(Entidad, os.path.join(subdir, e),
                               entidad_mapping,
                               transform=True, encoding='latin-1')
            lme.save(strict=True, verbose=verbose)
        for e in municipio:
            lme = LayerMapping(Municipio, os.path.join(subdir, e),
                               municipio_mapping,
                               transform=True, encoding='latin-1')
            lme.save(strict=True, verbose=verbose)
        for e in localidad:
            lme = LayerMapping(Localidad, os.path.join(subdir, e),
                               localidad_mapping,
                               transform=True, encoding='latin-1')
            lme.save(strict=True, verbose=verbose)
        for e in agebu:
            lme = LayerMapping(Agebu, os.path.join(subdir, e), agebu_mapping,
                               transform=True, encoding='latin-1')
            lme.save(strict=True, verbose=verbose)
        for e in agebr:
            lme = LayerMapping(Agebr, os.path.join(subdir, e), agebr_mapping,
                               transform=True, encoding='latin-1')
            lme.save(strict=True, verbose=verbose)
        for e in manzana:
            lme = LayerMapping(Manzana, os.path.join(subdir, e),
                               manzana_mapping,
                               transform=True, encoding='latin-1')
            lme.save(strict=True, verbose=verbose)


if __name__ == "__main__":
    run()
