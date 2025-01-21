# personal/scripts.py
from .models import CustomUser, Asistencia, Trabajador, AsistenciaCompleta
from django.db import transaction


def getFirstWord(string):
    space=string.find(" ")
    if space!=-1:
        return (string[0:space])
    return string.lower()

def generate_unique_username(base_username):
    counter = 1
    username=getFirstWord(base_username)
    while CustomUser.objects.filter(username=username).exists():
        username=f"{username}{counter}"
        counter += 1
    return username.lower()


def generate_asistencias_completas(trabajador):
    # Obtener todas las asistencias del trabajador, ordenadas por fecha y hora
    asistencias = Asistencia.objects.filter(trabajador=trabajador).order_by('finalFecha', 'finalHora')
    
    # Verificar si existen asistencias para el trabajador
    if not asistencias:
        return "No hay asistencias para este trabajador."

    # Obtener la última asistencia registrada y controlar la última procesada
    ultima_asistencia = Asistencia.objects.order_by('-finalFecha', '-finalHora').first()
    last_assistance = Asistencia.ultimaAsistenciaProcesada  # Última asistencia procesada

    # Si la última asistencia procesada ya está al día, no hacemos nada
    if last_assistance == ultima_asistencia.id:
        return "Ya se han procesado todas las asistencias."

    # Variable para gestionar el emparejamiento de entrada y salida
    entrada = None
    
    with transaction.atomic():  # Asegura la consistencia de los datos en caso de error
        for asistencia in asistencias:
            if asistencia.tipo == 'entrada':
                # Si es una entrada, la asignamos como entrada pendiente
                entrada = asistencia
            elif asistencia.tipo == 'salida' and entrada is not None:
                # Si encontramos una salida y ya tenemos una entrada pendiente
                AsistenciaCompleta.objects.create(
                    trabajador=trabajador,
                    entrada=entrada,
                    salida=asistencia
                )
                # Actualizamos la última asistencia procesada
                AsistenciaCompleta.ultimaAsistenciaProcesada = asistencia.id
                entrada = None  # Reiniciar la variable de entrada después de emparejar

        # Si la última asistencia fue una entrada sin salida, creamos una AsistenciaCompleta solo con la entrada
        if entrada is not None:
            AsistenciaCompleta.objects.create(
                trabajador=trabajador,
                entrada=entrada,
                salida=None  # No hay salida, solo la entrada
            )
            AsistenciaCompleta.ultimaAsistenciaProcesada = entrada.id  # Marcamos la entrada como la última procesada

    return "Asistencias completas generadas correctamente."
def completarAsistencias(trabajador):
    asistencias = list(Asistencia.objects.filter(trabajador=trabajador).order_by('-finalFecha', '-finalHora'))
    for i in range(len(asistencias)):
        print(i,": ",asistencias[i])

    
    
    

