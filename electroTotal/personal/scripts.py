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

def completarAsistencias(trabajador,last):
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
        
        
        
        
    
        
        

    
    
    

