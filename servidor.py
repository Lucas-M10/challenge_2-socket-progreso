from socket import *
from threading import Thread

#Lista que nos ayudara a guardar a los clientes que se van uniendo
clientes = []

def broadcast (mensaje:str, cliente_emisor:socket):

    mensaje_bytes = mensaje.encode ("utf-8")

    for cliente in clientes:

        if not cliente == cliente_emisor:
            cliente.send (mensaje_bytes)


#Funcion que se encarga de recibir el mensaje de los clientes
def manejar_cliente (cliente_socket:socket, cliente_address:tuple):

    while True:     
        #Rcibe mensaje del cliente  
        mensaje_cliente_bytes = cliente_socket.recv (1024)

        #Sino recibio un mensaje entonces cierra el bucle y cierra el socket 
        if not mensaje_cliente_bytes:
            #Removemos al cliente de la lista y cerramos el socket
            clientes.remove (cliente_socket)
            cliente_socket.close ()
            print (f"Se deconecto el cliente [{cliente_address[0]}:{cliente_address[1]}]")
            break
        
        #Imprimimos el mensaje del cliente
        mensaje_cliente = mensaje_cliente_bytes.decode ("utf-8")
        mensaje_id = f"[{cliente_address[0]}: {cliente_address[1]}]: {mensaje_cliente}"
        print (f"[{cliente_address[0]}:{cliente_address[1]}]: {mensaje_id}")

        #Llamo a la funcion que se encargara de reenviar los mensajes 
        broadcast (mensaje_cliente, cliente_socket)



#Creamos el socket y le decimos:
#Por donde van a viajar los datos (AF_INET) y como se van a transportar (SOCK_STREAM) 
server = socket(AF_INET, SOCK_STREAM)

#Creamos la direccion del server 
server.bind (("127.0.0.1", 5000))

#Le decimos que se quede esperando conexiones de clientes 
server.listen ()

#Loop que se encarga de aceptar a los clientes 
while True:

    #Aceptamos al cliente y recibos el mensaje como su direccion.
    cliente_socket, cliente_address = server.accept ()
    clientes.append (cliente_socket)
    nombre_bytes = cliente_socket.recv (1024)
    nombre_cliente = nombre_bytes.decode ("utf-8")

    print (f"""\n{nombre_cliente} se conecto desde:
ID: {cliente_address[0]}
Puerto: {cliente_address[1]}\n""")

    #Mensaje de bienvenida al cliente 
    # mensaje_servidor = "Hola Bienvenido al chat "
    # mensaje_bytes_servidor = mensaje_servidor.encode ("utf-8")
    # cliente_socket.send (mensaje_bytes_servidor)
    hilo = Thread (target=manejar_cliente, args=(cliente_socket, cliente_address))
    hilo.start ()
