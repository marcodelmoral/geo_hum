# This is an auto-generated Django model module created by ogrinspect.
from django.contrib.gis.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

entidad_mapping = {
    'cvegeo': 'CVEGEO',
    'cve_ent': 'CVE_ENT',
    'nomgeo': 'NOMGEO',
    'geom': 'MULTIPOLYGON',
}


# TODO Ponerle las propiedades de contenido en HTML para el mapa
# Poblacion por cada subdivision
# Quizas numero de subdivisiones
class Entidad(models.Model):
    # Identificacion geografica
    cvegeo = models.CharField(max_length=2)
    cve_ent = models.CharField(max_length=2)
    nomgeo = models.CharField(max_length=80)
    geom = models.MultiPolygonField(srid=4326)

    # Relacion de indicadores
    # Poblacion
    # Se deben permitir nulos puesto que hay datos que no estan en los datos de
    # INEGI pero no son 0
    # Se colocan los validadores:
    #       MaxValueValidator = valor maximo
    #       MinValueValidator = valor minimo
    # Se coloca el verbose_name, que es el nombre de la variable de INEGI
    # Se coloca el help_text, que es la descripcion y categoria del campo
    POBTOT = models.PositiveIntegerField(null=True,
                                         validators=[MaxValueValidator(2)],
                                         verbose_name='Población total',
                                         help_text='Total de personas que residen habitualmente en el país, entidad federativa, municipio y localidad. Incluye la estimación del número de personas en viviendas particulares sin información de ocupantes. Incluye a la población que no especificó su edad')
    POBMAS = models.PositiveIntegerField(null=True,
                                         verbose_name='Población masculina')
    POBFEM = models.PositiveIntegerField(null=True,
                                         verbose_name='Población femenina')
    P_0A2 = models.PositiveIntegerField(null=True,
                                        verbose_name='Población de 0 a 2 años')
    P_0A2_M = models.PositiveIntegerField(null=True,
                                          verbose_name='Población masculina de 0 a 2 años')
    P_0A2_F = models.PositiveIntegerField(null=True,
                                          verbose_name='Población femenina de 0 a 2 años')
    P_3YMAS = models.PositiveIntegerField(null=True,
                                          validators=[MinValueValidator(3),
                                                      MaxValueValidator(130)],
                                          verbose_name='Población de 3 años y más')

    def __str__(self):
        return self.nomgeo

    class Meta:
        ordering = ['nomgeo']


municipio_mapping = {
    'cvegeo': 'CVEGEO',
    'cve_ent': 'CVE_ENT',
    'cve_mun': 'CVE_MUN',
    'nomgeo': 'NOMGEO',
    'geom': 'MULTIPOLYGON',
}


class Municipio(models.Model):
    cvegeo = models.CharField(max_length=5)
    cve_ent = models.CharField(max_length=2)
    cve_mun = models.CharField(max_length=3)
    nomgeo = models.CharField(max_length=80)
    geom = models.MultiPolygonField(srid=4326)
    entidad = models.ForeignKey(Entidad, on_delete=models.SET_NULL, null=True)
    POBTOT = models.PositiveIntegerField(null=True,
                                         validators=[MaxValueValidator(2)],
                                         verbose_name='Población total',
                                         help_text='Total de personas que residen habitualmente en el país, entidad federativa, municipio y localidad. Incluye la estimación del número de personas en viviendas particulares sin información de ocupantes. Incluye a la población que no especificó su edad')
    POBMAS = models.PositiveIntegerField(null=True,
                                         verbose_name='Población masculina')
    POBFEM = models.PositiveIntegerField(null=True,
                                         verbose_name='Población femenina')
    P_0A2 = models.PositiveIntegerField(null=True,
                                        verbose_name='Población de 0 a 2 años')
    P_0A2_M = models.PositiveIntegerField(null=True,
                                          verbose_name='Población masculina de 0 a 2 años')
    P_0A2_F = models.PositiveIntegerField(null=True,
                                          verbose_name='Población femenina de 0 a 2 años')

    def __str__(self):
        return self.nomgeo

    def relaciona(self, created=False):
        if created:
            ent = Entidad.objects.get(cve_ent=self.cve_ent)
            ent.municipio_set.add(self)

    def save(self, *args, **kwargs):
        created = self.pk is None
        super(Municipio, self).save(*args, **kwargs)
        self.relaciona(created)

    class Meta:
        ordering = ['nomgeo']


localidad_mapping = {
    'cvegeo': 'CVEGEO',
    'cve_ent': 'CVE_ENT',
    'cve_mun': 'CVE_MUN',
    'cve_loc': 'CVE_LOC',
    'nomgeo': 'NOMGEO',
    'ambito': 'AMBITO',
    'geom': 'MULTIPOLYGON',
}


class Localidad(models.Model):
    cvegeo = models.CharField(max_length=9)
    cve_ent = models.CharField(max_length=2)
    cve_mun = models.CharField(max_length=3)
    cve_loc = models.CharField(max_length=4)
    nomgeo = models.CharField(max_length=120)
    ambito = models.CharField(max_length=6)
    geom = models.MultiPolygonField(srid=4326)
    entidad = models.ForeignKey(Entidad,
                                on_delete=models.SET_NULL,
                                null=True)
    municipio = models.ForeignKey(Municipio,
                                  on_delete=models.SET_NULL,
                                  null=True)
    POBTOT = models.PositiveIntegerField(null=True,
                                         validators=[MaxValueValidator(2)],
                                         verbose_name='Población total',
                                         help_text='Total de personas que residen habitualmente en el país, entidad federativa, municipio y localidad. Incluye la estimación del número de personas en viviendas particulares sin información de ocupantes. Incluye a la población que no especificó su edad')
    POBMAS = models.PositiveIntegerField(null=True,
                                         verbose_name='Población masculina')
    POBFEM = models.PositiveIntegerField(null=True,
                                         verbose_name='Población femenina')
    P_0A2 = models.PositiveIntegerField(null=True,
                                        verbose_name='Población de 0 a 2 años')
    P_0A2_M = models.PositiveIntegerField(null=True,
                                          verbose_name='Población masculina de 0 a 2 años')
    P_0A2_F = models.PositiveIntegerField(null=True,
                                          verbose_name='Población femenina de 0 a 2 años')

    def __str__(self):
        return self.nomgeo

    def relaciona(self, created=False):
        if created:
            ent = Entidad.objects.get(cve_ent=self.cve_ent)
            mun = ent.municipio_set.get(cve_mun=self.cve_mun)
            ent.localidad_set.add(self)
            mun.localidad_set.add(self)

    def save(self, *args, **kwargs):
        created = self.pk is None
        super(Localidad, self).save(*args, **kwargs)
        self.relaciona(created)

    class Meta:
        ordering = ['nomgeo']


agebu_mapping = {
    'cvegeo': 'CVEGEO',
    'cve_ent': 'CVE_ENT',
    'cve_mun': 'CVE_MUN',
    'cve_loc': 'CVE_LOC',
    'cve_ageb': 'CVE_AGEB',
    'geom': 'MULTIPOLYGON',
}


# Ageb urbano
class Agebu(models.Model):
    cvegeo = models.CharField(max_length=13)
    cve_ent = models.CharField(max_length=2)
    cve_mun = models.CharField(max_length=3)
    cve_loc = models.CharField(max_length=4)
    cve_ageb = models.CharField(max_length=4)
    geom = models.MultiPolygonField(srid=4326)
    entidad = models.ForeignKey(Entidad,
                                on_delete=models.SET_NULL,
                                null=True)
    municipio = models.ForeignKey(Municipio,
                                  on_delete=models.SET_NULL,
                                  null=True)
    localidad = models.ForeignKey(Localidad, on_delete=models.SET_NULL, null=True)
    POBTOT = models.PositiveIntegerField(null=True,
                                         validators=[MaxValueValidator(2)],
                                         verbose_name='Población total',
                                         help_text='Total de personas que residen habitualmente en el país, entidad federativa, municipio y localidad. Incluye la estimación del número de personas en viviendas particulares sin información de ocupantes. Incluye a la población que no especificó su edad')
    POBMAS = models.PositiveIntegerField(null=True,
                                         verbose_name='Población masculina')
    POBFEM = models.PositiveIntegerField(null=True,
                                         verbose_name='Población femenina')
    P_0A2 = models.PositiveIntegerField(null=True,
                                        verbose_name='Población de 0 a 2 años')
    P_0A2_M = models.PositiveIntegerField(null=True,
                                          verbose_name='Población masculina de 0 a 2 años')
    P_0A2_F = models.PositiveIntegerField(null=True,
                                          verbose_name='Población femenina de 0 a 2 años')

    def __str__(self):
        return self.cve_ageb

    def relaciona(self, created=False):
        if created:
            ent = Entidad.objects.get(cve_ent=self.cve_ent)
            mun = ent.municipio_set.get(cve_mun=self.cve_mun)
            loc = mun.localidad_set.get(cve_loc=self.cve_loc)
            ent.agebu_set.add(self)
            mun.agebu_set.add(self)
            loc.agebu_set.add(self)

    def save(self, *args, **kwargs):
        created = self.pk is None
        super(Agebu, self).save(*args, **kwargs)
        self.relaciona(created)


agebr_mapping = {
    'cvegeo': 'CVEGEO',
    'cve_ent': 'CVE_ENT',
    'cve_mun': 'CVE_MUN',
    'cve_ageb': 'CVE_AGEB',
    'geom': 'MULTIPOLYGON',
}


# Los ageb rurales no tienen localidad omg!
class Agebr(models.Model):
    cvegeo = models.CharField(max_length=9)
    cve_ent = models.CharField(max_length=2)
    cve_mun = models.CharField(max_length=3)
    cve_ageb = models.CharField(max_length=4)
    geom = models.MultiPolygonField(srid=4326)
    entidad = models.ForeignKey(Entidad,
                                on_delete=models.SET_NULL,
                                null=True)
    municipio = models.ForeignKey(Municipio,
                                  on_delete=models.SET_NULL,
                                  null=True)
    POBTOT = models.PositiveIntegerField(null=True, blank=True,
                                         validators=[MaxValueValidator(2)],
                                         verbose_name='Población total',
                                         help_text='Total de personas que residen habitualmente en el país, entidad federativa, municipio y localidad. Incluye la estimación del número de personas en viviendas particulares sin información de ocupantes. Incluye a la población que no especificó su edad')
    POBMAS = models.PositiveIntegerField(null=True, blank=True,
                                         verbose_name='Población masculina')
    POBFEM = models.PositiveIntegerField(null=True, blank=True,
                                         verbose_name='Población femenina')
    P_0A2 = models.PositiveIntegerField(null=True, blank=True,
                                        verbose_name='Población de 0 a 2 años')
    P_0A2_M = models.PositiveIntegerField(null=True, blank=True,
                                          verbose_name='Población masculina de 0 a 2 años')
    P_0A2_F = models.PositiveIntegerField(null=True, blank=True,
                                          verbose_name='Población femenina de 0 a 2 años')

    def __str__(self):
        return self.cve_ageb

    def relaciona(self, created=False):
        if created:
            ent = Entidad.objects.get(cve_ent=self.cve_ent)
            mun = ent.municipio_set.get(cve_mun=self.cve_mun)
            ent.agebr_set.add(self)
            mun.agebr_set.add(self)

    def save(self, *args, **kwargs):
        created = self.pk is None
        super(Agebr, self).save(*args, **kwargs)
        self.relaciona(created)


manzana_mapping = {
    'cvegeo': 'CVEGEO',
    'cve_ent': 'CVE_ENT',
    'cve_mun': 'CVE_MUN',
    'cve_loc': 'CVE_LOC',
    'cve_ageb': 'CVE_AGEB',
    'cve_mza': 'CVE_MZA',
    'ambito': 'AMBITO',
    'tipomza': 'TIPOMZA',
    'geom': 'MULTIPOLYGON',
}


class Manzana(models.Model):
    # Definicion de elementos para campo de eleccion

    CONJHAB_TIPO = ((1, 'Conjunto habitacional'),
                    (3, 'Manzana típica'),
                    (9, 'Manzana no especificada'))

    # Identificacion geografica

    cvegeo = models.CharField(max_length=16)
    cve_ent = models.CharField(max_length=2)
    cve_mun = models.CharField(max_length=3)
    cve_loc = models.CharField(max_length=4)
    cve_ageb = models.CharField(max_length=4)
    cve_mza = models.CharField(max_length=3)
    ambito = models.CharField(max_length=6)
    tipomza = models.CharField(max_length=16)
    geom = models.MultiPolygonField(srid=4326)
    entidad = models.ForeignKey(Entidad,
                                on_delete=models.SET_NULL,
                                null=True)
    municipio = models.ForeignKey(Municipio,
                                  on_delete=models.SET_NULL,
                                  null=True)
    localidad = models.ForeignKey(Localidad, on_delete=models.SET_NULL, null=True)
    agebu = models. ForeignKey(Agebu, on_delete=models.SET_NULL, null=True)
    agebr = models.ForeignKey(Agebr, on_delete=models.SET_NULL, null=True)

    # Relacion de indicadores
    # Poblacion
    POBTOT = models.PositiveIntegerField(null=True,
                                         validators=[MaxValueValidator(2)],
                                         verbose_name='Población total',
                                         help_text='Total de personas que residen habitualmente en el país, entidad federativa, municipio y localidad. Incluye la estimación del número de personas en viviendas particulares sin información de ocupantes. Incluye a la población que no especificó su edad')
    POBMAS = models.PositiveIntegerField(null=True,
                                         verbose_name='Población masculina')
    POBFEM = models.PositiveIntegerField(null=True,
                                         verbose_name='Población femenina')
    P_0A2 = models.PositiveIntegerField(null=True,
                                        verbose_name='Población de 0 a 2 años')
    P_0A2_M = models.PositiveIntegerField(null=True,
                                          verbose_name='Población masculina de 0 a 2 años')
    P_0A2_F = models.PositiveIntegerField(null=True,
                                          verbose_name='Población femenina de 0 a 2 años')

    # Infraestructura
    # Los nombres van sin el guin bajo!
    CONJHAB = models.PositiveSmallIntegerField(null=True, choices=CONJHAB_TIPO)

    def __str__(self):
        return self.cve_mza

    def relaciona(self, created=False):
        if created:
            ent = Entidad.objects.get(cve_ent=self.cve_ent)
            mun = ent.municipio_set.get(cve_mun=self.cve_mun)
            loc = mun.localidad_set.get(cve_loc=self.cve_loc)
            ent.manzana_set.add(self)
            mun.manzana_set.add(self)
            loc.manzana_set.add(self)
            if self.ambito == 'Urbana':
                agebu = loc.agebu_set.get(cve_ageb=self.cve_ageb)
                agebu.manzana_set.add(self)
            elif self.ambito == 'Rural':
                agebr = mun.agebr_set.get(cve_ageb=self.cve_ageb)
                agebr.manzana_set.add(self)

    def save(self, *args, **kwargs):
        created = self.pk is None
        super(Manzana, self).save(*args, **kwargs)
        self.relaciona(created)


