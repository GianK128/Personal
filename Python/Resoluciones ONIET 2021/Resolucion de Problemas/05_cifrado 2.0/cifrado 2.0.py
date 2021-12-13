# 
# GitHub: @GianK128
#

from sys import argv
import os

# Obtener la carpeta donde se encuentra el archivo
curr_dir = os.path.dirname(os.path.realpath(__file__))

# Mensaje de ayuda
if argv[1] == "-h":
    print("""
    Uso: python 'cifrado 2.0.py' [MODE] [KEY] [FILENAME].

    Arguments:
    - MODE: cifrar o descifrar el archivo, puede ser '-c' o '-d', respectivamente.
    - KEY: la key o el nuevo abecedario a partir del cual hacer la traduccion.
    - FILENAME: el nombre del archivo que se encuentra en ./data/ con su formato (.txt)
    """)
    exit(1)

# Validar argumentos
if len(argv) != 4: 
    print("ERROR: Faltan argumentos.")
    exit(1)

# Declarar variables de argumentos
param = argv[1]
key = argv[2]
file = f"{curr_dir}/data/{argv[3]}"

# Validar KEY
if len(set(key)) != 27: 
    print("ERROR: La KEY no tiene 27 caracteres, no es valida.")
    exit(1)

# Validar archivo
if not os.path.isfile(file): 
    print("ERROR: El archivo no existe")
    exit(1)

# Abecedario
ABC_REAL = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"

# Abecedario y clave en minuscula
ABC_REAL += ABC_REAL.lower()
key += key.lower()

# Validar parámetros y hacer la translation table
if param == "-c":
    trans_table = str.maketrans(ABC_REAL, key)
    new_file_str = "-cifrado.txt"
elif param == "-d":
    trans_table = str.maketrans(key, ABC_REAL)
    new_file_str = "-descifrado.txt"
else:
    print("ERROR: Parámetro invalido.\n Uso: python 'cifrado 2.0.py' [MODE] [KEY] [FILENAME]\n\n Use python 'cifrado 2.0.py' -h para más información.")
    exit(1)

# Leer archivo y traducir la string
with open(file, "r") as f:
    txt = f.read()
    translated = txt.translate(trans_table)

# Crear nuevo nombre de archivo transformado
new_file = file[:-4] + new_file_str

# Abrir o crear nuevo archivo y meterle la string traducida
with open(new_file, "w") as f:
    f.write(translated)

print("Traducido correctamente. Vaya a ./data/ para ver el archivo.")
