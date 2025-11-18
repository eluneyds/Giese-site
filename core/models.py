from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator


# ----------------- CATALOGOS -----------------

class TemaInteres(models.Model):
    descripcion_interes = models.CharField(max_length=150, unique=True)

    class Meta:
        db_table = "cuerpo_tema_interes"
        verbose_name = "Tema de interes"
        verbose_name_plural = "Temas de interes"
        ordering = ["descripcion_interes"]

    def __str__(self):
        return self.descripcion_interes


class Universidad(models.Model):
    descripcion_universidad = models.CharField(max_length=200, unique=True)

    class Meta:
        db_table = "cuerpo_universidad"
        verbose_name = "Universidad"
        verbose_name_plural = "Universidades"
        ordering = ["descripcion_universidad"]

    def __str__(self):
        return self.descripcion_universidad


class Nivel(models.Model):
    descripcion = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "cuerpo_nivel"
        verbose_name = "Nivel"
        verbose_name_plural = "Niveles"
        ordering = ["descripcion"]

    def __str__(self):
        return self.descripcion


# ----------------- INVESTIGACIÃ“N -----------------

class Investigacion(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    fecha = models.DateField(null=True, blank=True, verbose_name="Fecha de la investigacion")
    imagen_portada = models.ImageField(upload_to='investigaciones/portadas/', blank=True, null=True, verbose_name="Imagen de portada")
    video_portada = models.FileField(upload_to='investigaciones/videos/', blank=True, null=True, verbose_name="Video de portada", help_text="Archivo de video (MP4, WebM, etc.)")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="investigaciones",
        db_column="id_user",
        null=True, blank=True,
    )

    # RelaciÃ³n M2M con integrantes del equipo
    integrantes = models.ManyToManyField(
        'Equipo',
        through='InvestigacionIntegrante',
        related_name='investigaciones_participadas',
        blank=True
    )

    class Meta:
        ordering = ["-fecha"]
        db_table = "cuerpo_investigacion"
        verbose_name = "Investigacion"
        verbose_name_plural = "Investigaciones"

    def __str__(self):
        return self.titulo


class InvestigacionFoto(models.Model):
    investigacion = models.ForeignKey(
        Investigacion,
        on_delete=models.CASCADE,
        related_name="fotos",
        db_column="investigacion_id"
    )
    foto = models.ImageField(upload_to='investigaciones/fotos/', verbose_name="Foto")
    orden = models.IntegerField(default=0)

    class Meta:
        ordering = ["orden"]
        db_table = "cuerpo_investigacion_foto"

    def __str__(self):
        return f"Foto {self.id} de {self.investigacion.titulo}"


class InvestigacionArchivo(models.Model):
    investigacion = models.ForeignKey(
        Investigacion,
        on_delete=models.CASCADE,
        related_name="archivos",
        db_column="investigacion_id"
    )
    archivo = models.FileField(upload_to='investigaciones/archivos/', verbose_name="Archivo")
    nombre = models.CharField(max_length=200, blank=True, verbose_name="Nombre del archivo")
    orden = models.IntegerField(default=0)

    class Meta:
        ordering = ["orden"]
        db_table = "cuerpo_investigacion_archivo"

    def __str__(self):
        return self.nombre or f"Archivo {self.id}"


class InvestigacionIntegrante(models.Model):
    investigacion = models.ForeignKey(
        Investigacion,
        on_delete=models.CASCADE,
        db_column="investigacion_id"
    )
    integrante = models.ForeignKey(
        'Equipo',
        on_delete=models.CASCADE,
        db_column="integrante_id"
    )
    rol = models.CharField(max_length=100, blank=True, verbose_name="Rol en la investigacion")
    orden = models.IntegerField(default=0)

    class Meta:
        ordering = ["orden"]
        db_table = "cuerpo_investigacion_integrante"
        unique_together = (("investigacion", "integrante"),)

    def __str__(self):
        return f"{self.integrante.nombre} - {self.investigacion.titulo}"


# ----------------- AUTORES / PUBLICACIONES -----------------

class Autor(models.Model):
    """Autor interno (User) o externo por nombre/afiliacion."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='autores_perfil'
    )
    nombre = models.CharField(max_length=150, blank=True, default='')
    afiliacion = models.CharField(max_length=200, blank=True, default='')

    def __str__(self):
        if self.user_id:
            full = (self.user.get_full_name() or self.user.username).strip()
            return full
        return self.nombre or "(Autor)"


class Publicacion(models.Model):
    titulo = models.CharField(max_length=200)
    autores = models.CharField(max_length=200, blank=True)    # texto libre opcional
    resumen = models.TextField(blank=True)
    archivo = models.CharField(max_length=100, blank=True)    # texto/URL
    fecha = models.DateField(null=True, blank=True)
    imagen = models.CharField(max_length=100, blank=True)     # texto/URL
    video = models.CharField(max_length=100, blank=True)      # texto/URL

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="publicaciones",
        db_column="id_user",
        null=True, blank=True,
    )

    # Detalle de autores (M2M via intermedia)
    autores_detalle = models.ManyToManyField(
        Autor,
        through='PublicacionAutor',
        related_name='publicaciones',
        blank=True,
    )

    # Relación M2M con integrantes del equipo (similar a Investigacion)
    integrantes = models.ManyToManyField(
        'Equipo',
        through='PublicacionIntegrante',
        related_name='publicaciones_participadas',
        blank=True
    )

    class Meta:
        ordering = ["-fecha"]
        db_table = "cuerpo_publicacion"

    def __str__(self):
        return self.titulo


class PublicacionAutor(models.Model):
    ROL_CHOICES = (
        ('autor', 'Autor'),
        ('corresp', 'Autor de correspondencia'),
        ('editor', 'Editor'),
    )
    publicacion = models.ForeignKey('Publicacion', on_delete=models.CASCADE)
    autor = models.ForeignKey('Autor', on_delete=models.CASCADE)
    orden = models.PositiveIntegerField(default=1)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, blank=True, default='')

    class Meta:
        unique_together = (('publicacion', 'autor'),)
        db_table = "cuerpo_publicacionautor"
        ordering = ['orden']

    def __str__(self):
        return f"{self.publicacion_id} â€” {self.autor} ({self.rol or 'autor'})"


class PublicacionImagen(models.Model):
    publicacion = models.ForeignKey(
        "Publicacion",
        on_delete=models.CASCADE,
        db_column="publicacion_id",
        related_name="imagenes"
    )
    imagen = models.ImageField(upload_to='publicaciones/imagenes/', blank=True, null=True, verbose_name="Imagen")
    orden = models.IntegerField(default=0)

    class Meta:
        ordering = ["orden"]
        db_table = "cuerpo_publicacionimagen"

    def __str__(self):
        return f"Img {self.id} de {self.publicacion}"


class PublicacionVideo(models.Model):
    publicacion = models.ForeignKey(
        "Publicacion",
        on_delete=models.CASCADE,
        db_column="publicacion_id",
        related_name="videos"
    )
    video = models.FileField(upload_to='publicaciones/videos/', blank=True, null=True, verbose_name="Video")
    orden = models.IntegerField(default=0)

    class Meta:
        ordering = ["orden"]
        db_table = "cuerpo_publicacionvideo"

    def __str__(self):
        return f"Video {self.id} de {self.publicacion_id}"


class PublicacionArchivo(models.Model):
    publicacion = models.ForeignKey(
        "Publicacion",
        on_delete=models.CASCADE,
        db_column="publicacion_id",
        related_name="archivos"
    )
    archivo = models.FileField(upload_to='publicaciones/archivos/', verbose_name="Archivo")
    nombre = models.CharField(max_length=200, blank=True, verbose_name="Nombre del archivo")
    orden = models.IntegerField(default=0)

    class Meta:
        ordering = ["orden"]
        db_table = "cuerpo_publicacion_archivo"

    def __str__(self):
        return self.nombre or f"Archivo {self.id}"


class PublicacionIntegrante(models.Model):
    publicacion = models.ForeignKey(
        'Publicacion',
        on_delete=models.CASCADE,
        db_column="publicacion_id"
    )
    integrante = models.ForeignKey(
        'Equipo',
        on_delete=models.CASCADE,
        db_column="integrante_id"
    )
    rol = models.CharField(max_length=100, blank=True, verbose_name="Rol en la publicacion")
    orden = models.IntegerField(default=0)

    class Meta:
        ordering = ["orden"]
        db_table = "cuerpo_publicacion_integrante"
        unique_together = (("publicacion", "integrante"),)

    def __str__(self):
        return f"{self.integrante.nombre} - {self.publicacion.titulo}"


# ----------------- NOTICIAS -----------------

class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField(blank=True)
    fecha = models.DateField(null=True, blank=True, verbose_name="Fecha de la noticia")
    imagen = models.ImageField(upload_to='noticias/', blank=True, null=True, verbose_name="Imagen principal")
    video = models.FileField(upload_to='noticias/videos/', blank=True, null=True, verbose_name="Video", help_text="Archivo de video (MP4, WebM, etc.)")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="noticias",
        db_column="id_user",
        null=True, blank=True,
    )

    class Meta:
        ordering = ["-fecha"]
        db_table = "cuerpo_noticia"

    def __str__(self):
        return self.titulo


class NoticiaImagen(models.Model):
    noticia = models.ForeignKey(
        Noticia,
        on_delete=models.CASCADE,
        db_column="noticia_id",
        related_name="imagenes"
    )
    imagen = models.ImageField(upload_to='noticias/galeria/', blank=True, null=True, verbose_name="Imagen")
    orden = models.IntegerField(default=0)

    class Meta:
        ordering = ["orden"]
        db_table = "cuerpo_noticia_imagen"

    def __str__(self):
        return f"Imagen {self.id} de {self.noticia.titulo}"


# ----------------- EVENTOS -----------------

class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    fecha = models.DateField(null=True, blank=True)
    imagen_portada = models.ImageField(upload_to='eventos/portadas/', blank=True, null=True, verbose_name="Imagen de portada")
    color = models.CharField(max_length=7, blank=True, default="#2c5530", help_text="Color hex para acento, ej: #2c5530")
    pdf = models.CharField(max_length=100, blank=True)
    archivo = models.CharField(max_length=100, blank=True)
    fecha_cierre = models.DateField(null=True, blank=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="eventos",
        db_column="id_user",
        null=True, blank=True,
    )

    class Meta:
        ordering = ["-fecha"]
        db_table = "cuerpo_evento"

    def __str__(self):
        return self.nombre


class EventoArchivo(models.Model):
    evento = models.ForeignKey(
        "Evento",
        on_delete=models.CASCADE,
        db_column="evento_id",
        related_name="archivos"
    )
    archivo = models.FileField(upload_to='eventos/archivos/', verbose_name="Archivo")
    nombre = models.CharField(max_length=200, blank=True, verbose_name="Nombre del archivo")
    orden = models.IntegerField(default=0)

    class Meta:
        ordering = ["orden", "id"]
        db_table = "cuerpo_evento_archivo"

    def __str__(self):
        return self.nombre or (self.archivo.name if self.archivo else f"Archivo {self.id}")


# ----------------- EQUIPO -----------------

dni_validator = RegexValidator(
    regex=r"^\d{7,9}$",
    message="DNI debe contener al menos 7 dígitos."
)

class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    foto = models.CharField(max_length=100, blank=True)
    dni = models.CharField(
    max_length=9,
    unique=True,
    validators=[dni_validator],
    null=True,          # <--- permitir nulos por ahora
    blank=True,         # <--- que el form lo permita vacío
    help_text="Sólo números; 7–9 dígitos."
)
    nivel_descripcion = models.TextField(blank=True, verbose_name="Descripción del Nivel de Formación")
    linkedin_url = models.URLField(max_length=255, blank=True, verbose_name="URL de LinkedIn")
    email_publico = models.EmailField(max_length=255, blank=True, verbose_name="Email Público de Contacto")
    color_perfil = models.CharField(
        max_length=7,
        blank=True,
        default="#1a4d2e",
        verbose_name="Color de Perfil",
        help_text="Color en formato hexadecimal (ej. #1a4d2e) para la vista de perfil."
    )
    
    nivel = models.ForeignKey(
        Nivel,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        db_column="id_nivel",
        related_name="miembros"
    )
    universidades = models.ManyToManyField(
        Universidad,
        through="EquipoUniversidad",
        related_name="miembros",
        blank=True
    ) 

    intereses = models.ManyToManyField(
        TemaInteres,
        through="EquipoInteres",
        related_name="miembros",
        blank=True
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="equipos",
        db_column="id_user",
        null=True, blank=True,
    )

    class Meta:
        ordering = ["nombre"]
        db_table = "cuerpo_equipo"

    def __str__(self):
        return self.nombre


class EquipoInteres(models.Model):
    equipo = models.ForeignKey(
        Equipo,
        on_delete=models.CASCADE,
        db_column="id_equipo",
        related_name="equipo_intereses"
    )
    tema_interes = models.ForeignKey(
        TemaInteres,
        on_delete=models.CASCADE,
        db_column="id_tema_interes",
        related_name="equipo_intereses"
    )
    descripcion = models.TextField(blank=True, verbose_name="Descripción del Interés")
    orden = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = "cuerpo_equipo_interes"
        ordering = ["orden", "id"]
        unique_together = (("equipo", "tema_interes"),)

    def __str__(self):
        return f"{self.equipo} â€” {self.tema_interes} (orden {self.orden})"


class EquipoUniversidad(models.Model):
    equipo = models.ForeignKey(
        Equipo,
        on_delete=models.CASCADE,
        db_column="id_equipo",
        related_name="equipo_universidades"
    )
    universidad = models.ForeignKey(
        Universidad,
        on_delete=models.CASCADE,
        db_column="id_universidad",
        related_name="equipo_universidades"
    )
    descripcion = models.TextField(blank=True, verbose_name="Descripción (ej: Título obtenido)")
    orden = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = "cuerpo_equipo_universidad"
        ordering = ["orden", "id"]
        unique_together = (("equipo", "universidad"),)

    def __str__(self):
        return f"{self.equipo} â€” {self.universidad} (orden {self.orden})"


class Profesionalidad(models.Model):
    equipo = models.ForeignKey(
        Equipo,
        on_delete=models.CASCADE,
        db_column="id_equipo",
        related_name="profesionalidades"
    )
    titulo = models.CharField(max_length=150, verbose_name="Títuslo del Rol o Cargo")
    descripcion = models.TextField(blank=True, verbose_name="Descripción del Rol")
    orden = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = "cuerpo_equipo_profesionalidad"
        ordering = ["orden", "id"]
        verbose_name = "Profesionalidad"
        verbose_name_plural = "Profesionalidades"
    
    def __str__(self):
        return f"{self.equipo}: {self.titulo}"

