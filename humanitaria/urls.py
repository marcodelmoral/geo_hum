from django.urls import path

from humanitaria import views

app_name = 'humanitaria'

urlpatterns = [
    path('consulta_geo/', views.ConsultaGeoespacial.as_view(),
         name='consulta_geo'),
]
