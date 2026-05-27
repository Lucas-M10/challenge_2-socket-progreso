from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import time, sys

MAX_INTENTOS = 3

cliente = None
nombre = None

IP="127.0.0.1"
PORT = 5000

nombre = input ("Ingrese el nombre: ")
if nombre == "":
    nombre = "Anonimo"

#Funcion que se encarga de conectar y de la reconexion del cliente al servidor 
def intentar_conexion():
    global cliente

    for intento in range (MAX_INTENTOS):
        try:
            cliente = socket (AF_INET, SOCK_STREAM)
            cliente.connect((IP, PORT))
        
        except OSError:
            print (f"Error! Al conectarse quedan {intento+1}/{MAX_INTENTOS} intentos ")

            if intento <= MAX_INTENTOS-1:
                time.sleep (3)
            
            else:
                print (f"Error! No se pudo realizar la conexion")
                sys.exit()
                break

        else:
            nombre_bytes = nombre.encode ("utf-8")
            cliente.send (nombre_bytes)
            break

#Funcion que se encarga de la desconexion del cliente 
def desconectar_cliente ():
    try:
        print (f"Abandonamos el servidor")
        cliente.close ()

    except OSError:
        print (f"Ya se realizo la desconexion")


def recibir_mensaje ():
    while True:
        try:
            mensaje_bytes = cliente.recv (1024)

        except OSError as error:
            print (f"Error! Se cerro el servidor")

            if error.errno == 10054:
                intentar_conexion ()
                continue
            
            else:
                desconectar_cliente ()
                break
        
        else:
            mensaje = mensaje_bytes.decode ("utf-8")
            print (f"\n{mensaje}\n{nombre}: ", end="")


def enviar_mensaje ():
    while True:
        mensaje = input (f" ")

        if mensaje == "":
            print (f"Se abandono el servidor :(")
            desconectar_cliente(cliente)

        mensaje_bytes = mensaje.encode ("utf-8")

        try:
            cliente.send (mensaje_bytes)
        
        except OSError as error:
            

            if error.errno == 10054:
                intentar_conexion ()
                continue
            
            else:
                print (f"Error al enviar el mensaje")
                desconectar_cliente ()
                break


def main ():
    
    intentar_conexion ()

    hilo_1 = Thread (target=recibir_mensaje, daemon=True)
    hilo_2 = Thread (target=enviar_mensaje)

    hilo_1.start()
    hilo_2.start ()

main ()


            





