from socket import *
from threading import Thread

#Lista que nos ayudara a guardar a los clientes que se van uniendo
clientes = []

#Funcion que se encarga de enviar el mensaje a los clientes
def broadcast (mensaje:str, cliente_emisor:socket, nombre_cliente):

    mensaje_bytes = mensaje.encode ("utf-8")

    for cliente_socket, nombre in clientes.copy ():

        if not cliente_socket == cliente_emisor:

            try:
                cliente_socket.send (mensaje_bytes)

            except (OSError, ConnectionError) as error:
                print (f"Error {nombre} : {error}")
                desconectar_cliente (cliente_socket, None, nombre)


#Funcion que se encarga de sacar al cliente de la lista 
def desconectar_cliente (cliente_socket:socket, cliente_address:tuple , cliente_nombre:str ):

    if (cliente_socket, cliente_nombre) in clientes:

        clientes.remove ((cliente_socket, cliente_nombre))
    
    cliente_socket.close ()

    if cliente_address:
        print (f"""\n{cliente_nombre} se desconecto desde : 
ID: {cliente_address[0]}
Puerto: {cliente_address[1]}""")
        
    else:
        print (f"\n{cliente_nombre} se desconecto ")
        

#Funcion que se encarga de recibir el mensaje de los clientes
def manejar_cliente (cliente_socket:socket, cliente_address:tuple, nombre:str ):
    while True:

        try :     
            #Recibe mensaje del cliente  
            mensaje_cliente_bytes = cliente_socket.recv (1024)

        except (ConnectionError, OSError) as error:
            print (f"Error con {nombre}: {error} \n")
            desconectar_cliente (cliente_socket, cliente_address, nombre)
            break

        else: 

            #Sino recibio un mensaje entonces cierra el bucle y cierra el socket 
            if not mensaje_cliente_bytes:
                
                #Removemos al cliente de la lista y cerramos el socket
                desconectar_cliente (cliente_socket, cliente_address, nombre)
                break
            
            #Imprimimos el mensaje del cliente
            mensaje_cliente = mensaje_cliente_bytes.decode ("utf-8")
            mensaje_id = f"{nombre}: {mensaje_cliente}"
            print (f"{mensaje_id}")

            #Llamo a la funcion que se encargara de reenviar los mensajes 
            broadcast (mensaje_id, cliente_socket, nombre)


#Creamos el socket y le decimos:
#Por donde van a viajar los datos (AF_INET) y como se van a transportar (SOCK_STREAM) 
server = socket(AF_INET, SOCK_STREAM)

#Creamos la direccion del server 
server.bind (("127.0.0.1", 5000))

#Le decimos que se quede esperando conexiones de clientes 
server.listen ()

#Loop que se encarga de aceptar a los clientes 
while True:

    #Aceptamos al cliente y recibos el mensaje como su direccion
    cliente_socket, cliente_address = server.accept ()

    try:
        nombre_bytes = cliente_socket.recv (1024)

        nombre_cliente = nombre_bytes.decode ("utf-8")

    except (ConnectionError, OSError, UnicodeDecodeError) as error:

        print (f"Error: {error} ")
        cliente_socket.close ()
        continue

    else: 

        if not nombre_bytes:
            print ("Cliente se desconecto")
            cliente_socket.close ()
            continue

        clientes.append ((cliente_socket, nombre_cliente))

        #Se encarga de impimir el nombre del usuario 
        print (f"""\n{nombre_cliente} se conecto desde:
ID: {cliente_address[0]}
Puerto: {cliente_address[1]}\n""")

        hilo = Thread (target=manejar_cliente, args=(cliente_socket, cliente_address, nombre_cliente))
        hilo.start ()
