from threading import Lock, Thread
from socket import AF_INET, SOCK_STREAM, socket
import sys

IP = "127.0.0.1"
PORT = 5000

clientes = []

cliente_lock = Lock ()

# Funcion que crea el server 
def crear_server ():
    server = socket (AF_INET, SOCK_STREAM)
    server.bind((IP, PORT))
    server.listen ()
    return server

#Funcion que se encarga de reenviar los mensajes 
def broadcast (cliente_socket:socket, mensaje:str):
    
    for cliente in clientes.copy():

        #sino es el cliente que envio entonces envia el mensaje
        if not cliente == cliente_socket:
            mensaje_bytes = mensaje.encode ("utf-8")

            try :
                cliente.send(mensaje_bytes)

            except OSError:
                print (f"{cliente} se desconecto")
                desconectar_cliente (cliente, "Desconocido")       


# Se va a encargar de recibir los mensajes y de desconectar si es que se envio un vacio
def manejar_cliente (cliente_socket:socket, cliente_nombre):
    while True:

        #espera un mensaje si es que no recibe nada salta al bloque except
        try:
            mensaje_cliente_bytes = cliente_socket.recv (1024)

        #Imprimirmos un mensaje luego enviamos un mensaje de desconexion, cerramos el socket y cortamos el bucle
        except OSError:
            print (f"El cliente {cliente_nombre} se desconecto")
            mensaje_desconexion = f"{cliente_nombre} se desconecto"
            broadcast (cliente_socket, mensaje_desconexion)
            desconectar_cliente (cliente_socket, cliente_nombre)
            break

        #Si es que el mensaje llega vacio cerramos el socket y sino entonces mandamos el mensaje a todos 
        else:
            if not mensaje_cliente_bytes:

                print (f"{cliente_nombre} se desconecto")
                desconectar_cliente (cliente_socket, cliente_nombre)
                break

            else:
                mensaje_cliente = mensaje_cliente_bytes.decode ("utf-8")
                mensaje_cliente = f"{cliente_nombre}: {mensaje_cliente}"
                print (f"{mensaje_cliente}\n")
                broadcast (cliente_socket, mensaje_cliente)


#Funcion que se encarga de desconectar
def desconectar_cliente (cliente_socket:socket, cliente_nombre):
    #Bloqueamos la lista de clientes mientras removemos al cliente
    with cliente_lock:
        if cliente_socket in clientes:
            clientes.remove (cliente_socket)
    
    #Cerramos el socekt del cliente
    cliente_socket.close ()
    print (f"{cliente_nombre} abandono el server")

#Hilo principal que se encarga de aceptar a los clientes 
def aceptar_cliente (server:socket):
    server.settimeout (1)
    while True:

        #Acepta a los clientes que se van conectando 
        try:
            cliente_socket, cliente_address = server.accept ()

        except TimeoutError:
            continue

        mensaje = "Bienvenido al servidor"
        mensaje_bytes = mensaje.encode ("utf-8")
        
        #Si es que el cliente manda un nombre corre perfecto si se deconecta pasa al bloque except
        try:
            cliente_socket.send (mensaje_bytes)
            cliente_nombre = cliente_socket.recv (1024)

        #El bloque se encarga de cerrar el socket que fallo 
        except OSError:
            print (f"Se desconecto el cliente ")
            cliente_socket.close ()
            continue
        
        #Si no fallo en el try entonces asignamos un nombre si llego vacio sino entonces imprimimos el nombre 
        else:
            if not cliente_nombre:
                cliente_nombre = "Anonimo"

            cliente_nombre = cliente_nombre.decode ("utf-8")

            #Bloqueo la lista clientes para añadir un nuevo cliente
            with cliente_lock:
                clientes.append (cliente_socket)

            print (f"""\n{cliente_nombre} se conecto desde:
IP: {cliente_address[0]}
PORT: {cliente_address[1]}\n""")
            
            hilo = Thread (target=manejar_cliente, args= (cliente_socket, cliente_nombre), daemon=True)
            hilo.start()


server = crear_server()
aceptar_cliente (server)