import socket as s
import threading

#==========SETUP==========#

# CONTENIDO DE YAPA
SV_VERSION = "1.0"

# MACROS DE CONEXION
HEADER = 64
PORT = 5050
SERVER = s.gethostbyname(s.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'

# MACROS DE MENSAJES
MSG_DISCONNECT = "/close"
MSG_ONLY_USER = "Usted es el unico usuario conectado en este momento. Le avisaremos cuando se conecte alguien más.\n"
MSG_EXIT_CHAT = "/dc"

# LISTA DE EXCEPCIONES POSIBLES (Sirven más si luego se desea hacer una interfaz gráfica)
error_list = {
    "001" : "[ERROR #001] Hubo un error al crear un nuevo hilo de conexión.",
    "002" : "[ERROR #002] Hubo un problema en la conversión a str de la lista de usuarios.",
    "003" : "[ERROR #003] No se pudo completar el proceso de seleccion de usuario."
}

# Variables globales
conexiones = {}

# Crear conexion tcp
tcp = s.socket(s.AF_INET, s.SOCK_STREAM)
tcp.bind(ADDRESS)

#==========COMUNICACION CON CLIENTES==========#

def FormatListToString(what: list) -> str:
    return ''.join(f"{what[i]}\n" for i in range(len(what)))

def GetConnectionString(user: str) -> str:
    global conexiones

    try:
        # Quitar primero de la lista este usuario
        deleted_val = conexiones.pop(user)
        
        # Si la lista queda vacía avisar que es así y volver a agregar el usuario
        if not conexiones:
            conexiones[user] = deleted_val
            return MSG_ONLY_USER
        
        # Sacar las keys del dict, unpack y formato
        dict_keys = conexiones.keys()
        string = "\nInserte nombre de usuario de la persona con la que desea hablar.\n\n" + FormatListToString([*dict_keys])

        # Volver a agregar usuario a la lista para usarlo despues
        conexiones[user] = deleted_val

        # Unpack, formato y retornar
        return string
        
    except Exception as e:
        print(error_list['002'] +"\n" + str(e))
        return error_list['002']

def HandleChat(sender_conn: s.socket, receiver_user: str):
    global conexiones
    addr_to_send = conexiones[receiver_user]

    while True:
        try:
            msg = sender_conn.recv(HEADER)

            if msg == MSG_EXIT_CHAT:
                break

            sender_conn.sendto(msg, addr_to_send)

        except Exception as e:
            print(str(e))
            sender_conn.close()
            break

def ConnectionSendChoiceList(conexion: s.socket, direccion: tuple):
    global conexiones
    
    while True:
        try:
            # Esperar a recibir nombre de usuario y decodificarlo
            user = conexion.recv(HEADER).decode(FORMAT)

            # Chequear si el usuario ya esta registrado
            if user not in conexiones:
                conexiones[user] = direccion
                print(f"\n[REGISTRO EXITOSO] Se registró un nuevo usuario '{user}', con la dirección {direccion}")
            else:
                print("\n[REGISTRO FALLIDO] Se intentó registrar un usuario, pero ya existe el registro.")
                continue
            
            # Loop hasta seleccionar usuario correctamente
            while True:
                # Obtener lista sin este usuario y mandarla
                conn_list = GetConnectionString(user)
                conexion.send(conn_list.encode(FORMAT))

                # Esperar respuesta por nombre de usuario y mostrar
                user_selected = conexion.recv(HEADER).decode(FORMAT)
                print(user_selected)

                # Chequear si el usuario sigue conectado
                if user_selected in conexiones:
                    break
                else:
                    conexion.send("[CHAT] El usuario está desconectado".encode(FORMAT))
                    continue

            # Empezar funcion de chat con este usuario
            conexion.send("[CHAT] Usuario encontrado. Iniciando conexión...".encode(FORMAT))
            HandleChat(conexion, user_selected)

        except Exception as e:
            print(error_list['003'] + f" ({direccion})\n" + str(e))
            break
    
    conexion.close()

    # TODO: Chequear si alguno de los mensajes es una desconexión

    # TODO: Volver a enviar lista a todos los no conectados cuando se conecta uno nuevo, en caso de que esten esperando
    
#==========PROGRAMA PRINCIPAL==========#

def main():
    global tcp
    tcp.listen()

    while True:
        # Esperar hasta que alguien se conecte
        conn, addr = tcp.accept()

        try:
            # Crear un nuevo hilo para la conexión.
            thread = threading.Thread(target = ConnectionSendChoiceList, args = (conn, addr))
            thread.start()

        except Exception as e:
            print(error_list['001'] + '\n' + str(e))
            conn.close()
            tcp.close()
            break

if __name__ == "__main__":
    print(f"[BIENVENIDO] Python Chat-TCP Server v{SV_VERSION}.")
    print(f"[ARRANCANDO SERVIDOR] Servidor escuchando en {ADDRESS}")
    main()