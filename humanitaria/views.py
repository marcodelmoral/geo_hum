import json

from django.shortcuts import render
from django.views.generic.edit import FormView

from humanitaria.forms import FormConsultaGeo
from humanitaria.serializers import *


class ConsultaGeoespacial(FormView):
    template_name = 'consulta_geoespacial2.html'
    form_class = FormConsultaGeo

    def form_invalid(self, form):
        return super(ConsultaGeoespacial, self).form_invalid(form)

    def form_valid(self, form):
        entidad = form.cleaned_data['entidad']
        municipio = form.cleaned_data['municipio']
        # localidad = form.cleaned_data['localidad']
        # agebu = form.cleaned_data['agebu']
        # agebr = form.cleaned_data['agebr']
        ent = None
        mun = None
        loc = None
        agu = None
        agr = None
        mza = None
        # La búsqueda es por municipio, ojo!
        if entidad:
            ent = EntidadSerializer(entidad.municipio_set.all(),
                                    many=True).data
            if municipio:
                mun = MunicipioSerializer(municipio).data

                loc = LocalidadSerializer(municipio.localidad_set.all(),
                                          many=True).data
                # if agebu:
                agu = AgebuSerializer(municipio.agebu_set.all(),
                                          many=True).data

                # if agebr:
                agr = AgebrSerializer(municipio.agebr_set.all(),
                                          many=True).data
                mza = ManzanaSerializer(municipio.manzana_set.all(),
                                        many=True).data
        else:
            ent = EntidadSerializer(Entidad.objects.all(), many=True).data

        return render(self.request,
                      self.template_name,
                      {'form': form,
                       'entidad': json.dumps(ent),
                       'municipio': json.dumps(mun),
                       'localidad': json.dumps(loc),
                       'agebu': json.dumps(agu),
                       'agebr': json.dumps(agr),
                       'manzana': json.dumps(mza)})
