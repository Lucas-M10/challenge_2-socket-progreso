from socket import *
from threading import Thread

#Funcion que se encarga de recibir el mensaje de los clientes
def manejar_cliente (cliente_socket:socket, cliente_address:tuple):

    while True:       
        mensaje_cliente_bytes = cliente_socket.recv (1024)

        if not mensaje_cliente_bytes:
            cliente_socket.close ()
            print ("Se deconecto el cliente ")
            break
    
        mensaje_cliente = mensaje_cliente_bytes.decode ("utf-8")
        print (f"[{cliente_address[0]}:{cliente_address[1]}]: {mensaje_cliente}")

        mensaje_servidor = input (f"responde a [{cliente_address[0]}:{cliente_address[1]}]: ")
        if mensaje_servidor =="":
            print (f"Se cerro el chat con el cliente [{cliente_address[0]}:{cliente_address[1]}]")
            cliente_socket.close ()
            break
        else:    
            mensaje_bytes_servidor = mensaje_servidor.encode ()
            cliente_socket.send (mensaje_bytes_servidor)


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
    print (f"""\nEl cliente se conecto desde:
    ID: {cliente_address[0]}
    Puerto: {cliente_address[1]}\n""")

    #Mensaje de bienvenida al cliente 
    mensaje_servidor = "Hola Bienvenido al chat "
    mensaje_bytes_servidor = mensaje_servidor.encode ("utf-8")
    cliente_socket.send (mensaje_bytes_servidor)
    hilo = Thread (target=manejar_cliente, args=(cliente_socket, cliente_address))
    hilo.start ()
