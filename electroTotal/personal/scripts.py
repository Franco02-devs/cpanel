# personal/scripts.py
from .models import CustomUser, Asistencia, Trabajador, AsistenciaCompleta


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

def completarAsistencias(trabajador):
    last=trabajador.ultimaAsistenciaProcesada   
    asistencias = list(Asistencia.objects.filter(trabajador=trabajador,id__gte=last))
    print(asistencias)
    entrada = None
    
    for i in range(len(asistencias)):
        asistencia = asistencias[i]
        
        if getFirstWord(asistencia.tipo) == 'entrada':
            entrada = asistencia
        else:
            if entrada is not None:
                AsistenciaCompleta.objects.get_or_create(
                    trabajador=trabajador,
                    entrada=entrada,
                    salida=asistencia,
                )
                entrada = None
    
    if entrada is not None:
        AsistenciaCompleta.objects.get_or_create(
            trabajador=trabajador,
            entrada=entrada,
            salida=None,
        )
def limpiarAsistenciasIncompletas(trabajador):
    asistencias =list(AsistenciaCompleta.objects.filter(trabajador=trabajador))
    asistencia=None
    for i in range(len(asistencias)-1):
        asistencia = asistencias[i]
        if asistencia.salida is None:
            asistencia.delete()
    if asistencia.salida is not None:
        ultimaAsistencia=asistencia.salida
        print(ultimaAsistencia.id)
        trabajador.ultimaAsistenciaProcesada=int(ultimaAsistencia.id)
        trabajador.save()
        
def corregirFecha(asistencia):
    if asistencia.fecha_diferida:
        asistencia.finalFecha=asistencia.fecha_diferida
        asistencia.fecha_diferida=None
        asistencia.tipo=getFirstWord(asistencia.tipo)
        asistencia.save()

def corregirAllFecha():
    asistencias = Asistencia.objects.all()

    for asistencia in asistencias:
        try:
            corregirFecha(asistencia)
        except Exception as e:
            print(f"Error al corregir la asistencia {asistencia.id}: {e}")
            
def completarLimpiarAll():
    trabajadores = Trabajador.objects.all()

    for trabajador in trabajadores:
        try:
            completarAsistencias(trabajador)
            limpiarAsistenciasIncompletas(trabajador)
        except Exception as e:
            print(f"Error al corregir la asistencia {trabajador.id}: {e}")
            
def diferenciaFecha(fecha_inicio, fecha_fin):
    if fecha_inicio and fecha_fin:
        # Calculamos la diferencia entre las fechas
        diferencia = fecha_fin - fecha_inicio
        
        # Extraemos las horas, minutos y segundos
        horas = diferencia.days * 24 + diferencia.seconds // 3600
        minutos = (diferencia.seconds % 3600) // 60
        segundos = diferencia.seconds % 60
        
        # Devuelves la diferencia en formato horas:minutos:segundos
        return f'{horas:02}:{minutos:02}:{segundos:02}'
    return None


    
    
