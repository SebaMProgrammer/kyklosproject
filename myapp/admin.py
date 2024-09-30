from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.html import format_html
from .models import Empleado, Tarea, PuestosDelDia
from django.core.exceptions import ValidationError
import re


# Validador personalizado para el RUT
def validar_rut(value):
    if not re.match(r'^\d{8}[0-9Kk]$', value):  # Verifica que el formato sea correcto (8 números y un dígito verificador)
        raise ValidationError('El RUT debe tener 8 números seguidos de un dígito verificador (número o K).')

# Formatear el RUT en el formato solicitado
def formatear_rut(rut):
    rut = rut.upper()
    return f"{rut[:-8]}.{rut[-8:-5]}.{rut[-5:-2]}-{rut[-1]}"

# Formulario personalizado para mostrar la imagen y validar el RUT
class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = '__all__'

    rut = forms.CharField(validators=[validar_rut])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['imagen'].help_text = format_html(
                '<img src="{}" style="max-width: 150px; height: auto;" />',
                self.instance.imagen.url if self.instance.imagen else '/media/default.jpg'
            )


# Administración del modelo con formato del RUT y validación
class EmpleadoAdmin(admin.ModelAdmin):
    form = EmpleadoForm
    list_display = ['nombre', 'apellido', 'rut_formateado', 'horario', 'activo', 'imagen_tag']

    def rut_formateado(self, obj):
        return formatear_rut(obj.rut)
    
    rut_formateado.short_description = 'RUT'

    def imagen_tag(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="width: 60px; height: 60px;" />'.format(obj.imagen.url))
        else:
            return format_html('<img src="/media/default.jpg" style="width: 60px; height: 60px;" />')

    imagen_tag.short_description = 'Imagen'

class PuestosDelDiaForm(forms.ModelForm):
    class Meta:
        model = PuestosDelDia
        fields = '__all__'

    # Definir los widgets para los campos ManyToMany con FilteredSelectMultiple
    mesa_1_empleados = forms.ModelMultipleChoiceField(
        queryset=Empleado.objects.all(),
        required=False,
        widget=FilteredSelectMultiple('Empleados Mesa 1', is_stacked=False)
    )
    mesa_1_tareas = forms.ModelMultipleChoiceField(
        queryset=Tarea.objects.all(),
        required=False,
        widget=FilteredSelectMultiple('Tareas Mesa 1', is_stacked=False)
    )

    mesa_2_empleados = forms.ModelMultipleChoiceField(
        queryset=Empleado.objects.all(),
        required=False,
        widget=FilteredSelectMultiple('Empleados Mesa 2', is_stacked=False)
    )
    mesa_2_tareas = forms.ModelMultipleChoiceField(
        queryset=Tarea.objects.all(),
        required=False,
        widget=FilteredSelectMultiple('Tareas Mesa 2', is_stacked=False)
    )

    mesa_3_empleados = forms.ModelMultipleChoiceField(
        queryset=Empleado.objects.all(),
        required=False,
        widget=FilteredSelectMultiple('Empleados Mesa 3', is_stacked=False)
    )
    mesa_3_tareas = forms.ModelMultipleChoiceField(
        queryset=Tarea.objects.all(),
        required=False,
        widget=FilteredSelectMultiple('Tareas Mesa 3', is_stacked=False)
    )

    mesa_4_empleados = forms.ModelMultipleChoiceField(
        queryset=Empleado.objects.all(),
        required=False,
        widget=FilteredSelectMultiple('Empleados Mesa 4', is_stacked=False)
    )
    mesa_4_tareas = forms.ModelMultipleChoiceField(
        queryset=Tarea.objects.all(),
        required=False,
        widget=FilteredSelectMultiple('Tareas Mesa 4', is_stacked=False)
    )

    # Validación para que un empleado no esté en más de una mesa
    def clean(self):
        cleaned_data = super().clean()

        # Obtener los empleados asignados a cada mesa
        mesa_1_empleados = cleaned_data.get('mesa_1_empleados')
        mesa_2_empleados = cleaned_data.get('mesa_2_empleados')
        mesa_3_empleados = cleaned_data.get('mesa_3_empleados')
        mesa_4_empleados = cleaned_data.get('mesa_4_empleados')

        # Combinar todos los empleados asignados
        empleados_asignados = set()
        mesas = [mesa_1_empleados, mesa_2_empleados, mesa_3_empleados, mesa_4_empleados]

        # Revisar si algún empleado está en más de una mesa
        for mesa in mesas:
            if mesa:  # Verificar que no sea None
                for empleado in mesa:
                    if empleado in empleados_asignados:
                        raise forms.ValidationError(f"El empleado {empleado} ya está asignado a otra mesa.")
                    empleados_asignados.add(empleado)

        # Validación para que no haya más de un PuestoDelDia con la misma fecha y horario
        fecha = cleaned_data.get('fecha')
        horario = cleaned_data.get('horario')

        if PuestosDelDia.objects.filter(fecha=fecha, horario=horario).exists():
            raise forms.ValidationError(f"Ya existe una fila de PuestosDelDia para la fecha {fecha} y el horario {horario}.")

        return cleaned_data


class PuestosDelDiaAdmin(admin.ModelAdmin):
    form = PuestosDelDiaForm  # Asignamos el formulario personalizado

    # Mostrar campos relevantes en la lista del admin
    list_display = ['fecha', 'horario', 'creado_por']

    # Removemos "creado_por" del formulario para que no sea editable
    exclude = ['creado_por']

    # Sobrescribimos el método save_model para asignar el usuario actual al campo creado_por
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Si es una nueva instancia
            obj.creado_por = request.user  # Asignar el usuario actual al campo creado_por
        super().save_model(request, obj, form, change)


# Registrar los modelos en el admin
admin.site.register(Empleado, EmpleadoAdmin)
admin.site.register(Tarea)
admin.site.register(PuestosDelDia, PuestosDelDiaAdmin)