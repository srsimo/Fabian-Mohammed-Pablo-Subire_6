# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""
##Ejercicio 1
def TresenTres(max):
    for i in range(max):
        if(i % 3 == 0):
            print(i)
        
num = 7
TresenTres(num)

##Ejercicio 2
from datetime import datetime

def Fechas():
    hoy = datetime.today()
    print(hoy)
    print(str(hoy.year) + "-" + str(hoy.month) + "-" + str(hoy.day) + " " + str(hoy.hour) + ":" + str(hoy.minute) 
          + ":" + str(hoy.second))
    
Fechas()

##Ejercicio 3
frase = 'En un lugar de La Mancha, de cuyo nombre no quiero acordarme'

def AlReves(frase):
    print(frase[::-1])
    
AlReves(frase)

##Ejercicio 4

def cambiar_dominio(correos, nuevo_dominio="ces.es"):
    nuevos_emails = []
    for email in correos:
        nombre = email.split("@")[0]
        nuevos_emails.append(nombre + "@" + nuevo_dominio)
    return nuevos_emails

correos = ["pablo@gmail.com", "fabian@hotmail.com", "alexia@yahoo.es"]
nuevos_correos = cambiar_dominio(correos)
print(nuevos_correos)
    
    
    
    