from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

HOST = "127.0.0.1"
PORT = 5000

nombre = input ("Nombre de usuario: ")
if nombre == "":
    nombre = "anonimo"

#Creo el socket
cliente = socket(AF_INET, SOCK_STREAM)

#Me conecto al servidor pasandole la direccion y puerto que utilizaremos 
cliente.connect ((HOST, PORT))

#Le envio el nombre como primer mensaje al servidor luego entra en el loop
nombre_bytes = nombre.encode ("utf-8")
cliente.send (nombre_bytes)

#Funcion que se encarga de recibir los mensajes e imprimir en pantalla 
def recibir_mensaje ():
    while True:
        mensaje_bytes= cliente.recv (1024)

        if not mensaje_bytes:
            cliente.close ()
            print ("Un usuario abandono el chat")
            break

        mensaje = mensaje_bytes.decode ("utf-8")
        print (f"\n{mensaje}\n usuario: ", end="", flush=True)
 
#Funcion que se encarga de enviar los mensajes 
def enviar_mensaje ():
    while True :
        mensaje = input ("")

        if mensaje == "":
            cliente.close ()
            print ("Se abandondo el chat ")
            break
        
        mensaje_bytes = mensaje.encode ("utf-8")
        cliente.send (mensaje_bytes)


#Creamos los hilos e Iniciamos 
hilo_enviar = Thread (target= enviar_mensaje)
hilo_recibir = Thread (target= recibir_mensaje)

hilo_enviar.start ()
hilo_recibir.start ()


