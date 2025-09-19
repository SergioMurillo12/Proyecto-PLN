from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_textos, name='lista_textos'),
    path('subir/', views.subir_texto, name='subir_texto'),
]
