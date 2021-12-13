import socket as s
import threading

#==========SETUP==========#

# CONTENIDO DE YAPA
CL_VERSION = "1.0"

# MACROS DE CONEXION
HEADER = 256
PORT = 5050
SERVER = s.gethostbyname(s.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'

# MACROS DE PERFIL
USERNAME = ""

# MACROS DE MENSAJES
MSG_DISCONNECT = '/close'
MSG_ONLY_USER = "Usted es el unico usuario conectado en este momento. Le avisaremos cuando se conecte alguien más.\n"

# Variables globales
connected_to_user = False

# Crear conexion udp
client = s.socket(s.AF_INET, s.SOCK_STREAM)
client.connect(ADDRESS)

#==========PROGRAMA PRINCIPAL==========#

def main():
    global USERNAME
    global client
    global connected_to_user

    USERNAME = input("Ingrese su nombre de usuario: ")
    client.send(USERNAME.encode(FORMAT))

    while True:
        # Enviar nombre de usuario y recibir la respuesta (la lista de usuarios)
        # TODO: Header dinámico
        # TODO: Comando para cerrar conexión
        users_connected = client.recv(HEADER).decode(FORMAT)

        # Si es el unico usuario, se queda esperando a otra llamada del servidor
        if users_connected == MSG_ONLY_USER:
            while True:
                print("[ESPERANDO...]")

                wakeup_call = client.recv(HEADER).decode(FORMAT)
                print(wakeup_call)
                break
            continue

        # Mostrar la lista de usuarios
        print(users_connected)

        # Esperar por entrada para ver con quien se quiere conectar, y enviar
        user_selected = input()
        client.send(user_selected.encode(FORMAT))

        connected_to_user = True

        # Ya debería haber empezado el chat
        while True:
            msg = input("Mensaje: ")
            client.send(msg.encode(FORMAT))

if __name__ == "__main__":
    print(f"[BIENVENIDO] Python Chat-TCP Client v{CL_VERSION}.")
    main()