from rest_framework_gis.serializers import GeoFeatureModelSerializer

from humanitaria.models import *

GEOM_FIELD = 'geom'
FIELDS = ('contenido', 'nomgeo')


class EntidadSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = Entidad
        geo_field = GEOM_FIELD

        fields = FIELDS


class MunicipioSerializer(GeoFeatureModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """

    class Meta:
        model = Municipio
        geo_field = GEOM_FIELD

        fields = FIELDS


class LocalidadSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = Localidad
        geo_field = GEOM_FIELD

        fields = FIELDS


class AgebuSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = Agebu
        geo_field = GEOM_FIELD

        fields = FIELDS


class AgebrSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = Agebr
        geo_field = GEOM_FIELD

        fields = FIELDS


class ManzanaSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = Manzana
        geo_field = GEOM_FIELD

        fields = FIELDS
