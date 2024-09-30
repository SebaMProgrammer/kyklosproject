from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from .models import PuestosDelDia

def home(request):
    fecha_hora_actual = timezone.now()
    horario_default = 'M' if fecha_hora_actual.hour < 13 else 'T'
    
    # Si el usuario ha enviado el formulario, se usa el horario seleccionado manualmente
    horario_actual = request.POST.get('horario', horario_default)

    # Filtrar los PuestosDelDia por la fecha actual y el horario seleccionado
    puestos = PuestosDelDia.objects.filter(fecha=fecha_hora_actual.date(), horario=horario_actual).first()

    empleados = []
    if puestos:
        # Recolecta los empleados de las mesas 1 a 4
        empleados_mesa_1 = puestos.mesa_1_empleados.all()
        empleados_mesa_2 = puestos.mesa_2_empleados.all()
        empleados_mesa_3 = puestos.mesa_3_empleados.all()
        empleados_mesa_4 = puestos.mesa_4_empleados.all()

        for empleado in empleados_mesa_1:
            empleados.append({'nombre': empleado.nombre, 'apellido': empleado.apellido, 'mesa': 'Mesa 1'})
        for empleado in empleados_mesa_2:
            empleados.append({'nombre': empleado.nombre, 'apellido': empleado.apellido, 'mesa': 'Mesa 2'})
        for empleado in empleados_mesa_3:
            empleados.append({'nombre': empleado.nombre, 'apellido': empleado.apellido, 'mesa': 'Mesa 3'})
        for empleado in empleados_mesa_4:
            empleados.append({'nombre': empleado.nombre, 'apellido': empleado.apellido, 'mesa': 'Mesa 4'})

    return render(request, 'home.html', {
        'fecha_hora': fecha_hora_actual,
        'empleados': empleados,
        'horario_actual': horario_actual
    })

def actualizar_puestos(request):
    horario = request.GET.get('horario')
    fecha_actual = timezone.now().date()

    # Filtrar los PuestosDelDia por la fecha actual y el horario seleccionado
    puestos = PuestosDelDia.objects.filter(fecha=fecha_actual, horario=horario)

    empleados_mesa = []
    for puesto in puestos:
        empleados_mesa.append({
            'mesa': 'Mesa 1',
            'empleados': list(puesto.mesa_1_empleados.values('nombre', 'apellido'))
        })
        empleados_mesa.append({
            'mesa': 'Mesa 2',
            'empleados': list(puesto.mesa_2_empleados.values('nombre', 'apellido'))
        })
        empleados_mesa.append({
            'mesa': 'Mesa 3',
            'empleados': list(puesto.mesa_3_empleados.values('nombre', 'apellido'))
        })
        empleados_mesa.append({
            'mesa': 'Mesa 4',
            'empleados': list(puesto.mesa_4_empleados.values('nombre', 'apellido'))
        })

    return JsonResponse({'empleados_mesa': empleados_mesa})
