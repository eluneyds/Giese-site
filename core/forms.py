from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import ( # AsegÃºrate de importar EquipoUniversidad
    Equipo, Noticia, Investigacion, Publicacion, Evento,
    TemaInteres, Universidad, Nivel, EquipoInteres
)

# ---------- Equipo ----------
class EquipoForm(forms.ModelForm):
    
    class Meta:
        model = Equipo
        fields = [
            'nombre', 'descripcion', 'nivel_descripcion', 
            'foto', 'dni', 'linkedin_url', 'email_publico',
            'color_perfil'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nombre completo',
                'id': 'id_nombre'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': 'Informacion profesional, especialidad, etc.',
                'id': 'id_descripcion'
            }),
            'nivel_descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Detalles especificos sobre la formacion (Ej: Tesis sobre...)',
                'id': 'id_nivel_descripcion'
            }),
            'foto': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'https://ejemplo.com/imagen.jpg',
                'id': 'id_foto_url'
            }),
            'dni': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Solo numeros (7–9 digitos)',
                'pattern': r'\d{7,9}',
                'id': 'id_dni'
            }),
            'linkedin_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://linkedin.com/in/usuario',
                'id': 'id_linkedin_url'
            }),
            'email_publico': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com',
                'id': 'id_email_publico'
            }),
            'color_perfil': forms.TextInput(attrs={
                'type': 'color',
                'class': 'form-control form-control-color',
                'id': 'id_color_perfil',
                'title': 'Seleccione un color para el perfil'
            }),
        }
        # Hacemos que el campo de URL de la foto no sea requerido a nivel de modelo en el form
        field_classes = {'foto': forms.CharField}
    
    # Campos adicionales para funcionalidades mejores
    foto_archivo = forms.FileField(
        required=False,
        label="Subir archivo de imagen",
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*',
            'id': 'id_foto_archivo'
        }),
        help_text="PNG, JPG o URL abajo"
    )
    
    nuevo_tema_interes = forms.CharField(
        required=False,
        max_length=150,
        label="Agregar tema de interes",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Investigacion educativa',
            'id': 'id_nuevo_tema_interes'
        })
    )

    nueva_universidad = forms.CharField(
        required=False,
        max_length=200,
        label="Agregar otra universidad",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Facultad de Derecho, Universidad X',
            'id': 'id_nueva_universidad'
        })
    )
    
    # Campo libre para el nivel (texto), se mapea a modelo Nivel en save()
    nivel_text = forms.CharField(
        required=False,
        label="Nivel de formacion mas alto",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Licenciatura, Maestria, Doctorado, Tecnicatura...',
            'id': 'id_nivel'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Prefill nivel_text desde la instancia
        instance = kwargs.get('instance') or getattr(self, 'instance', None)
        if instance and getattr(instance, 'nivel_id', None) and instance.nivel:
            self.fields['nivel_text'].initial = instance.nivel.descripcion

    def save(self, commit=True):
        equipo = super().save(commit=False)
        # Mapear nivel_text -> Nivel (FK)
        nivel_valor = (self.cleaned_data.get('nivel_text') or '').strip()
        if nivel_valor:
            nivel_obj, _ = Nivel.objects.get_or_create(descripcion=nivel_valor)
            equipo.nivel = nivel_obj
        else:
            # Si quedo vacio, permitimos limpiar el FK
            equipo.nivel = None

        if commit:
            equipo.save()
        return equipo


# ---------- Login ----------
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'autofocus': True, 'class': 'form-control', 'placeholder': 'Usuario'
    }))
    password = forms.CharField(label="Contraseña", strip=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Contraseña'
    }))


# ---------- Noticia ----------
class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ['titulo', 'contenido', 'imagen', 'video', 'fecha']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titulo de la noticia'}),
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Contenido de la noticia'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'video': forms.FileInput(attrs={'class': 'form-control', 'accept': 'video/*'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


# ---------- InvestigaciÃ³n ----------
class InvestigacionForm(forms.ModelForm):
    class Meta:
        model = Investigacion
        fields = ['titulo', 'descripcion', 'imagen_portada', 'video_portada', 'fecha']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titulo de la investigacion'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Descripción, resumen, objetivos, etc.'}),
            'imagen_portada': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'video_portada': forms.FileInput(attrs={'class': 'form-control', 'accept': 'video/*'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


# ---------- PublicaciÃ³n ----------
class PublicacionForm(forms.ModelForm):
    """
    Formulario completo para Publicaciones, que permite gestionar campos de texto
    y relaciones como imÃ¡genes, videos, archivos e integrantes, que se procesan
    en la vista.
    """
    class Meta:
        model = Publicacion
        fields = ['titulo', 'autores', 'resumen', 'fecha']
        widgets = {
            'titulo':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titulo de la publicacion'}),
            'autores': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: A. Perez, M. Lopez, J. Diaz'}),
            'resumen': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Resumen, detalles, etc.'}),
            'fecha':   forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


# ---------- Evento ----------
class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nombre', 'fecha', 'fecha_cierre', 'descripcion', 'imagen_portada', 'color', 'pdf', 'archivo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del evento'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_cierre': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descripcion del evento'}),
            'imagen_portada': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control form-control-color'}),
            'pdf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ruta o URL del PDF'}),
            'archivo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ruta o URL del archivo'}),
        }

