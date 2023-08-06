import logging  #Muestra mensajes en consola. Por default warning o superior

from codigofranco.workshops import unreleased   #Ejecutar funciones desde una librería

"""
INFO -> 10
DEBUG -> 20
WARNING -> 30
ERROR -> 40
CRITICAL -> 50
"""
logging.basicConfig(level=logging.INFO)

#Ejecuta todo lo del bloque si y solo si este archivo se ejecuta como principal
if __name__ == '__main__':
    logging.debug(">>> Estamos comenzando la ejecución del paquete")
    #Es una buena práctica reemplazar todos los print por logging al crear una librería
    workshops = unreleased()
    #logging.debug(help(unreleased)) #Muestra el docstring

    logging.debug(">>> Estamos finalizando la ejecución del paquete")