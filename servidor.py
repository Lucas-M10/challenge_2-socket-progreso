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
print (f"El cliente se conecto desde {cliente_address}\n")

#Mensaje de bienvenida al cliente 
mensaje_servidor = "Hola Bienvenido al chat"
mensaje_bytes_servidor = mensaje_servidor.encode ("utf-8")
cliente_socket.send (mensaje_bytes_servidor)


#Le decimos que va a recibir el mensaje y le damos un valor maximo de bytes del mensaje 
mensaje_bytes_cliente = cliente_socket.recv (1024)
mensaje_cliente = mensaje_bytes_cliente.decode ("utf-8")
print (mensaje_cliente)


cliente_socket.close ()

server.close ()