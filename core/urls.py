# core/urls.py
from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    # pÃºblicas
    path("", views.inicio, name="inicio"),
    path("equipo/", views.equipo, name="equipo"),
    path("equipo/<int:pk>/", views.equipo_detalle, name="equipo_detalle"),
    path("noticias/", views.noticias, name="noticias"),
    path("investigacion/", views.investigacion, name="investigacion"),
    path("investigacion/<int:pk>/", views.investigacion_detalle, name="investigacion_detalle"),
    path("publicaciones/", views.publicaciones, name="publicaciones"),
    path("publicaciones/<int:pk>/", views.publicacion_detalle, name="publicacion_detalle"),
    path("eventos/", views.eventos, name="eventos"),
    path("eventos/<int:pk>/", views.evento_detalle, name="evento_detalle"),
    path("contacto/", views.contacto, name="contacto"),

    # auth
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # panel equipo
    path("panel/equipo/", views.panel_equipo, name="panel_equipo"),
    path("panel/equipo/add/", views.equipo_add, name="equipo_add"),
    path("panel/equipo/<int:pk>/edit/", views.equipo_edit, name="equipo_edit"),
    path("panel/equipo/<int:pk>/delete/", views.equipo_delete, name="equipo_delete"),

    # panel noticias
    path("panel/noticias/", views.panel_noticias, name="panel_noticias"),
    path("panel/noticias/add/", views.noticia_add, name="noticia_add"),
    path("panel/noticias/<int:pk>/edit/", views.noticia_edit, name="noticia_edit"),
    path("panel/noticias/<int:pk>/delete/", views.noticia_delete, name="noticia_delete"),

    # panel investigacion
    path("panel/investigacion/", views.panel_investigacion, name="panel_investigacion"),
    path("panel/investigacion/add/", views.investigacion_add, name="investigacion_add"),
    path("panel/investigacion/<int:pk>/edit/", views.investigacion_edit, name="investigacion_edit"),
    path("panel/investigacion/<int:pk>/delete/", views.investigacion_delete, name="investigacion_delete"),

    # panel publicaciones
    path("panel/publicaciones/", views.panel_publicaciones, name="panel_publicaciones"),
    path("panel/publicaciones/add/", views.publicacion_add, name="publicacion_add"),
    path("panel/publicaciones/<int:pk>/edit/", views.publicacion_edit, name="publicacion_edit"),
    path("panel/publicaciones/<int:pk>/delete/", views.publicacion_delete, name="publicacion_delete"),

    # panel eventos
    path("panel/eventos/", views.panel_eventos, name="panel_eventos"),
    path("panel/eventos/add/", views.evento_add, name="evento_add"),
    path("panel/eventos/<int:pk>/edit/", views.evento_edit, name="evento_edit"),
    path("panel/eventos/<int:pk>/delete/", views.evento_delete, name="evento_delete"),
    path("panel/eventos/<int:pk>/", views.evento_detalle, name="evento_detalle"),
]

