# core/admin.py
from django.contrib import admin
from .models import (
    Equipo, EquipoInteres, EquipoUniversidad, Profesionalidad, TemaInteres, Universidad, Nivel,
    Noticia, NoticiaImagen, 
    Investigacion, InvestigacionFoto, InvestigacionArchivo, InvestigacionIntegrante,
    Publicacion, PublicacionImagen, PublicacionIntegrante, Evento,
    Autor, PublicacionAutor
)

# ===================== Catálogos =====================

@admin.register(TemaInteres)
class TemaInteresAdmin(admin.ModelAdmin):
    list_display = ("id", "descripcion_interes")
    search_fields = ("descripcion_interes",)
    ordering = ("descripcion_interes",)


@admin.register(Universidad)
class UniversidadAdmin(admin.ModelAdmin):
    list_display = ("id", "descripcion_universidad")
    search_fields = ("descripcion_universidad",)
    ordering = ("descripcion_universidad",)


@admin.register(Nivel)
class NivelAdmin(admin.ModelAdmin):
    list_display = ("id", "descripcion")
    search_fields = ("descripcion",)
    ordering = ("descripcion",)


# ===================== Equipo =====================

class EquipoInteresInline(admin.TabularInline):
    """
    Permite gestionar los intereses del integrante desde Equipo.
    Usa la tabla intermedia para poder definir el 'orden'.
    """
    model = EquipoInteres
    extra = 1
    autocomplete_fields = ("tema_interes",)
    fields = ("tema_interes", "orden")
    ordering = ("orden",)


class EquipoUniversidadInline(admin.TabularInline):
    """
    Permite gestionar las universidades del integrante desde Equipo.
    Usa la tabla intermedia para poder definir el 'orden'.
    """
    model = EquipoUniversidad
    extra = 1
    autocomplete_fields = ("universidad",)
    fields = ("universidad", "orden")
    ordering = ("orden",)


class ProfesionalidadInline(admin.TabularInline):
    """
    Permite gestionar los roles/profesionalidades del integrante.
    """
    model = Profesionalidad
    extra = 1
    fields = ("titulo", "descripcion", "orden")
    ordering = ("orden",)


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "dni", "nivel", "color_perfil", "user")
    search_fields = (
        "nombre", "dni",
        "user__username", "user__first_name", "user__last_name", "user__email",
        "profesionalidades__titulo", # Buscar en los tÃ­tulos de los roles
    )
    list_filter = ("nivel",)
    inlines = [ProfesionalidadInline, EquipoUniversidadInline, EquipoInteresInline]
    autocomplete_fields = ("nivel", "user")
    ordering = ("nombre",)

    fieldsets = (
        (None, {
            "fields": ("nombre", "dni", "user")
        }),
        ("Perfil PÃºblico", {
            "fields": ("descripcion", "foto", "linkedin_url", "email_publico", "color_perfil")
        }),
        ("FormaciÃ³n AcadÃ©mica", {
            "fields": ("nivel", "nivel_descripcion")
        }),
    )


# ===================== Noticias =====================

class NoticiaImagenInline(admin.TabularInline):
    model = NoticiaImagen
    extra = 1
    fields = ("imagen", "orden")
    ordering = ("orden",)


@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "fecha", "user")
    search_fields = ("titulo",)
    list_filter = ("fecha",)
    autocomplete_fields = ("user",)
    inlines = [NoticiaImagenInline]
    ordering = ("-fecha", "titulo")


# ===================== InvestigaciÃ³n =====================

class InvestigacionFotoInline(admin.TabularInline):
    model = InvestigacionFoto
    extra = 1
    fields = ("foto", "orden")
    ordering = ("orden",)


class InvestigacionArchivoInline(admin.TabularInline):
    model = InvestigacionArchivo
    extra = 1
    fields = ("archivo", "nombre", "orden")
    ordering = ("orden",)


class InvestigacionIntegranteInline(admin.TabularInline):
    model = InvestigacionIntegrante
    extra = 1
    autocomplete_fields = ("integrante",)
    fields = ("integrante", "rol", "orden")
    ordering = ("orden",)


@admin.register(Investigacion)
class InvestigacionAdmin(admin.ModelAdmin):
    list_display = ("titulo", "fecha", "user")
    search_fields = ("titulo",)
    list_filter = ("fecha",)
    autocomplete_fields = ("user",)
    inlines = [InvestigacionFotoInline, InvestigacionArchivoInline, InvestigacionIntegranteInline]
    ordering = ("-fecha", "titulo")


# ===================== PublicaciÃ³n =====================

class PublicacionImagenInline(admin.TabularInline):
    model = PublicacionImagen
    extra = 0
    fields = ("imagen", "orden")
    ordering = ("orden",)


class PublicacionAutorInline(admin.TabularInline):
    model = PublicacionAutor
    extra = 1
    autocomplete_fields = ("autor",)
    fields = ("autor", "rol", "orden")
    ordering = ("orden",)


class PublicacionIntegranteInline(admin.TabularInline):
    model = PublicacionIntegrante
    extra = 1
    autocomplete_fields = ("integrante",)
    fields = ("integrante", "rol", "orden")
    ordering = ("orden",)


@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    list_display = ("titulo", "fecha", "user")
    search_fields = ("titulo", "autores")
    list_filter = ("fecha",)
    autocomplete_fields = ("user",)
    inlines = [PublicacionAutorInline, PublicacionIntegranteInline, PublicacionImagenInline]
    ordering = ("-fecha", "titulo")


# ===================== Evento =====================

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "fecha", "fecha_cierre", "user")
    search_fields = ("nombre",)
    list_filter = ("fecha", "fecha_cierre")
    autocomplete_fields = ("user",)
    fieldsets = (
        (None, {"fields": ("nombre", "fecha", "fecha_cierre", "descripcion", "user")}),
        ("Archivos", {"fields": ("pdf", "archivo")}),
    )
    ordering = ("-fecha", "nombre")


# ===================== Autor =====================

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ("__str__", "afiliacion", "user")
    search_fields = (
        "nombre", "afiliacion",
        "user__username", "user__first_name", "user__last_name", "user__email",
    )
    autocomplete_fields = ("user",)
    ordering = ("nombre",)

