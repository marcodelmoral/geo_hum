from crispy_forms.bootstrap import Field
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from django.forms import Form, ModelChoiceField
from django_select2.forms import ModelSelect2Widget

from humanitaria.models import *


class FormConsultaGeo(Form):

    entidad = ModelChoiceField(
        queryset=Entidad.objects.all(),
        label="Entidad",
        required=False,
        widget=ModelSelect2Widget(
            model=Entidad,
            search_fields=['nomgeo__icontains'],
        )
    )
    municipio = ModelChoiceField(
        queryset=Municipio.objects.all(),
        label="Municipio",
        required=False,
        widget=ModelSelect2Widget(
            model=Municipio,
            search_fields=['nomgeo__icontains'],
            dependent_fields={'entidad': 'entidad'},
        )
    )

    localidad = ModelChoiceField(
        queryset=Localidad.objects.all(),
        label="Localidad",
        required=False,
        widget=ModelSelect2Widget(
            model=Localidad,
            search_fields=['nomgeo__icontains'],
            dependent_fields={'municipio': 'municipio'},
        )
    )

    ageu = ModelChoiceField(
        queryset=Localidad.objects.all(),
        label="AGEB Urbama",
        required=False,
        widget=ModelSelect2Widget(
            model=Agebu,
            search_fields=['cve_ageb__icontains'],
            dependent_fields={'localidad': 'localidad'},
        )
    )

    ager = ModelChoiceField(
        queryset=Localidad.objects.all(),
        label="AGEB Rural",
        required=False,
        widget=ModelSelect2Widget(
            model=Agebr,
            search_fields=['cve_ageb__icontains'],
            dependent_fields={'municipio': 'municipio'},
        )
    )

    def __init__(self, *args, **kwargs):
        super(FormConsultaGeo, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit',
                                     'Buscar',
                                     css_class='btn-success'))
        self.helper.form_class = 'form'
        self.helper.help_text_inline = True
        self.helper.layout = Layout(
            Field('entidad', css_class=''),
            Field('municipio'),
            Field('localidad'),
        )
