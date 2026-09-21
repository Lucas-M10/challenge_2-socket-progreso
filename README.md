# Chat Multi-Cliente en Tiempo Real (Sockets TCP)

Sistema de mensajería grupal y comunicación bidireccional cliente-servidor desarrollado en **Python**, utilizando sockets TCP nativos (`socket`) y programación concurrente con hilos (`threading`) junto con control de concurrencia mediante cerrojos (`Lock`).

---

## 📋 Descripción General

El proyecto implementa una arquitectura cliente-servidor distribuida para mensajería en tiempo real. Permite que múltiples clientes se conecten simultáneamente a un servidor centralizado, envíen mensajes de texto y los distribuyan a todos los participantes conectados mediante un mecanismo de difusión (*broadcast*).

Incluye manejo robusto de excepciones de red, desconexiones limpias, control de accesos a memoria compartida y reintentos automáticos de reconexión.

---

## ✨ Características Principales

### Servidor (`servidor.py`)
- **Arquitectura Concurrente:** Atiende múltiples clientes en paralelo creando un hilo dedicado (`Thread`) para escuchar las entradas de cada uno.
- **Sincronización Segura (`threading.Lock`):** Protege la lista de sockets activos (`clientes`) de condiciones de carrera (*race conditions*) durante las operaciones de alta y baja.
- **Mecanismo de Broadcast:** Reenvía los mensajes a todos los clientes conectados, exceptuando al emisor original.
- **Handshake Inicial:** Transmite un mensaje de bienvenida y solicita el nombre identificador del usuario al conectarse.
- **Tolerancia a Fallos y Timeout:** Utiliza un timeout de socket para evitar bloqueos indefinidos al aceptar conexiones y gestiona desconexiones abruptas notificando al resto de la sala.

### Cliente (`cliente.py`)
- **I/O No Bloqueante (Multihilo):** Separa la captura de entrada por consola (`input`) y la recepción continua de mensajes del servidor en dos hilos independientes.
- **Reconexión Automática:** Cuenta con un bucle de reintentos (`MAX_INTENTOS = 3`) con espera escalonada y captura de errores de conexión (`WinError 10054` / `10053`).
- **Desconexión Voluntaria:** Permite salir del chat enviando un mensaje vacío (presionando `Enter`), cerrando el socket y liberando los recursos de forma ordenada.

---

## 🛠️ Tecnologías Utilizadas

- **Lenguaje:** Python 3.8 o superior
- **Módulos Estándar (sin dependencias externas):**
  - `socket`: Creación y gestión de sockets de flujo TCP (`AF_INET`, `SOCK_STREAM`).
  - `threading`: Hilos concurrentes (`Thread`) y mecanismos de sincronización (`Lock`).
  - `time`: Control de retardos en la reconexión.
  - `sys`: Operaciones del sistema en tiempo de ejecución.

---

## 🚀 Instalación y Puesta en Marcha

### 1. Clonar el repositorio
```bash
git clone https://github.com/Lucas-M10/challenge_2-socket-progreso.git
cd challenge_2-socket-progreso
```

### 2. Configuración de Red
Por defecto, ambos scripts se comunican en la dirección local de loopback:
- **IP:** `127.0.0.1` (localhost)
- **Puerto:** `5000`

> **Nota:** Para ejecutar el chat entre diferentes computadoras en una misma red local (LAN), edita la variable `IP` en `cliente.py` colocando la dirección IPv4 del equipo donde se ejecuta el servidor.

---

## 💻 Modo de Uso

### Paso 1: Iniciar el Servidor
En una primera terminal, arranca el servidor:
```bash
python servidor.py
```
El servidor quedará a la espera de nuevas conexiones en el puerto 5000 y registrará la IP y puerto de cada cliente conectado.

### Paso 2: Conectar Clientes
Abre una terminal nueva por cada cliente que desees simular y ejecuta:
```bash
python cliente.py
```

1. Ingresa tu nombre o alias cuando lo solicite:
   ```text
   Ingrese el nombre: Lucas
   ```
2. Recibirás el mensaje de bienvenida y podrás empezar a escribir mensajes:
   ```text
   Bienvenido al servidor
   Lucas: Hola a todos!
   ```
3. Los demás clientes conectados recibirán el mensaje con el formato `Nombre: Mensaje`.
4. Para abandonar la sala, pulsa la tecla **Enter** con el campo vacío.

---

## 📂 Estructura del Proyecto

```text
challenge_2-socket-progreso/
├── cliente.py     # Lógica del cliente, hilos de I/O y reconexión TCP
├── servidor.py    # Servidor concurrente, difusión (broadcast) y sincronización con Lock
└── README.md      # Documentación técnica del proyecto
```

---

## 👤 Autor

- **Lucas-M10** - [Perfil de GitHub](https://github.com/Lucas-M10)
