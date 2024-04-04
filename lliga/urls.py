from django.contrib import admin
from django.urls import path, include

from lliga import views


urlpatterns = [
    path('menu', views.menu, name="menu"),
    path('classificacio/<int:lliga_id>', views.classificacio, name="classificacio"),
    path('crearLliga', views.crearLliga, name="crearLliga"),
    path('crearEquip', views.crearEquip, name="crearEquip"),
    # path('editarEquip', views.editarEquip, name="editarEquip"),
    path('editarEquip', views.editar_equip, name="editar_equip"),
]