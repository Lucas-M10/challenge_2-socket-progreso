from socket import socket, AF_INET, SOCK_STREAM

HOST = "127.0.0.1"
PORT = 5000

cliente = socket(AF_INET, SOCK_STREAM)

#Me conecto al servidor pasandole la direccion y puerto que utilizaremos 
cliente.connect ((HOST, PORT))

#Recibimos el mensaje que envia el servidro 
mensaje_servidor_bytes = cliente.recv (1024)
mensaje_servidor = mensaje_servidor_bytes.decode ("utf-8")
print (mensaje_servidor)

#Mandamos mensaje al servidor 
mensaje_cliente = "Hola servidor soy el cliente 1"
mensaje_cliente_bytes  = mensaje_cliente.encode ("utf-8")
cliente.send (mensaje_cliente_bytes)

cliente.close ()