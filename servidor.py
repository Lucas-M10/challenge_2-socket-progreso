from socket import *

#Creamos el socket y le decimos:
#Por donde van a viajar los datos (AF_INET) y como se van a transportar (SOCK_STREAM) 
server = socket(AF_INET, SOCK_STREAM)

#Creamos la direccion del server 
server.bind (("127.0.0.1", 5000))

#Le decimos que se quede esperando conexiones de clientes 
server.listen ()


#Aceptamos al cliente y recibos el mensaje como su direccion.
cliente_socket, cliente_address = server.accept ()
print (f"""\nEl cliente se conecto desde:
ID: {cliente_address[0]}
Puerto: {cliente_address[1]}\n""")

#Mensaje de bienvenida al cliente 
mensaje_servidor = "Hola Bienvenido al chat "
mensaje_bytes_servidor = mensaje_servidor.encode ("utf-8")
cliente_socket.send (mensaje_bytes_servidor)

#aca creamos el while el loop donde va a estar recibiendo el mensaje de los clientes
while True:
    mensaje_cliente_bytes = cliente_socket.recv (1024) 

    if mensaje_cliente_bytes:

        mensaje_cliente = mensaje_cliente_bytes.decode ("utf-8")
        print (f"Cliente: {mensaje_cliente}" )
        mensaje_servidor = input ("servidor: ")
        mensaje_bytes_servidor = mensaje_servidor.encode ("utf-8")
        cliente_socket.send (mensaje_bytes_servidor)
    
    else:
        print ("Se cierra el chat")
        break

cliente_socket.close ()
server.close ()