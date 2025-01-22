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
        
def ajustar_errores():
    print("daa")
    print("daa")
    print("daa")
    print("daa")
    print("daa")
    
    
        

    
        
        
        
        
    
        
        

    
    
    

