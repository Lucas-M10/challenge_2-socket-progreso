from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import time, sys

MAX_INTENTOS = 3

cliente = None

IP="127.0.0.1"
PORT = 5000

nombre = input ("Ingrese el nombre: ")

#Funcion que se encarga de conectar y de la reconexion del cliente al servidor 
def intentar_conexion():
    global cliente

    #Va a intententar ingresar hasta la cantidad maxima de intentos
    for intento in range (MAX_INTENTOS):
        
        try:
            cliente = socket (AF_INET, SOCK_STREAM)
            cliente.connect((IP, PORT))
        
        except OSError:
            print (f"Error! Al conectarse quedan {intento+1}/{MAX_INTENTOS} intentos ")

            if intento < MAX_INTENTOS-1:
                time.sleep (3)
            
            else:
                print (f"Error! No se pudo realizar la conexion")
                print (f"presione ENTER para salir")
                desconectar_cliente ()
                
        else:
            nombre_bytes = nombre.encode ("utf-8")
            cliente.send (nombre_bytes)
            break


#Funcion que se encarga de la desconexion del cliente 
def desconectar_cliente ():
    try:
        cliente.close ()

    except OSError as error:
        print (f"{error}: al intentar desconectar al cliente")


#Funcion que se encarga de recibir los mensajes
def recibir_mensaje ():
      while True:
        try:
            mensaje_bytes= cliente.recv (1024)

        except OSError as error:
            # print(f"Error al recibir el mensaje: \n{error}")

            if error.errno == 10054 :
                intentar_conexion ()
                continue

            elif error.errno == 10053:
                desconectar_cliente()
                break

            else:
                desconectar_cliente ()
                break

        else:

            if not mensaje_bytes:
                desconectar_cliente()
                break
            
            mensaje = mensaje_bytes.decode ("utf-8")
            print (f"\n{mensaje}\n{nombre}: ", end="",)


#Funcion recibir mensaje
def enviar_mensaje():
    while True :
        mensaje = input ("")

        if mensaje == "":
            print ("Se abandondo el chat ")
            desconectar_cliente ()
            break
        
        mensaje_bytes = mensaje.encode ("utf-8")

        try:
            cliente.send (mensaje_bytes)

        except  OSError as error:
            
            if error.errno == 10054 :
                intentar_conexion ()
                continue
            
            else:
                print (f"Error al enviar mensaje: {error}")
                desconectar_cliente ()
                break

def main ():
    
    intentar_conexion()

    hilo_1 = Thread (target=enviar_mensaje)
    hilo_2 = Thread (target=recibir_mensaje)
                    
    hilo_1.start ()
    hilo_2.start ()

main ()

