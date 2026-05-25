from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import sys
import time

HOST = "127.0.0.1"
PORT = 5000
MAX_INTENTOS = 3


nombre = input ("Nombre de usuario: ")
if nombre == "":
    nombre = "Anonimo"

#Creo el socket
cliente =None

def intentar_conexion ():
#Me conecto al servidor pasandole la direccion y puerto que utilizaremos 
    global cliente
    for intentos in range(MAX_INTENTOS):
        try:
            cliente = socket (AF_INET, SOCK_STREAM)
            cliente.connect ((HOST, PORT))


        except ConnectionRefusedError:
            print (f"Intento {intentos +1} de {MAX_INTENTOS} ")
            
            if intentos <MAX_INTENTOS-1:
                time.sleep (3)
            
            else:
                print (f"No se pudo conectar al servidor ")
                sys.exit ()
        
        else:
            cliente.send (nombre.encode("utf-8"))
            break


#Funcion que se encarga de desconectar correcctamente
def desconectar_cliente ():

    try:
        cliente.close ()

    except OSError as error:
        print (f"{error}: al intentar desconectar al cliente")


#Funcion que se encarga de recibir los mensajes e imprimir en pantalla 
def recibir_mensaje ():

    while True:
        try:
            mensaje_bytes= cliente.recv (1024)

        except (ConnectionResetError, OSError) as error:
            print(f"Error al recibir el mensaje: \n{error}")

            if error.errno == 10054 :
                intentar_conexion ()
                continue
            else:
                desconectar_cliente ()
                break

        else:

            if not mensaje_bytes:
                desconectar_cliente()
                break

            mensaje = mensaje_bytes.decode ("utf-8")
            print (f"\n{mensaje}\n{nombre}: ", end="", flush=True)
 

#Funcion que se encarga de enviar los mensajes 
def enviar_mensaje ():

    while True :
        mensaje = input ("")

        if mensaje == "":
            print ("Se abandondo el chat ")
            desconectar_cliente ()
            break
        
        mensaje_bytes = mensaje.encode ("utf-8")

        try:
            cliente.send (mensaje_bytes)

        except (BrokenPipeError, ConnectionResetError, OSError) as error:
            
            if error.errno == 10054 :
                intentar_conexion ()
                continue
            
            else:
                print (f"Error al enviar mensaje: {error}")
                desconectar_cliente ()
                break

#Creamos los hilos e Iniciamos 
intentar_conexion ()

hilo_enviar = Thread (target= enviar_mensaje)
hilo_recibir = Thread (target= recibir_mensaje)

hilo_enviar.start ()
hilo_recibir.start ()