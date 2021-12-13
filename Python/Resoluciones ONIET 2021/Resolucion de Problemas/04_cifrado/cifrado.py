# 
# GitHub: @GianK128
#

from sys import argv

# Chequear que se reciban la cantidad de argumentos correctos.
if len(argv) != 2:
    print("Usage: python cifrado_keberlein.py KEY")
    exit(1)

# Chequear que la clave otorgada no tenga caracteres repetidos y tenga 27 caracteres. Tambien que sean puras letras.
if len(set(argv[1])) != 27 or not argv[1].isalpha():
    print("La clave no es valida. Debe tener 27 caracteres y no repetirse.")
    exit(1)

# Declarar globales del abecedario real y pasar la clave a mayusculas para conveniencia.
ABC_REAL = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
KEY = argv[1].upper()

# Funcion de cifrado
def CifrarConClave(texto: str) -> str:
    """
        Devuelve el texto que se le pasa y lo cifra con la KEY otorgada, basandose en la posicion de cada letra en el abecedario.

        `texto`: la string a cifrar.
    """
    # Declarar string a la que se le van a ir agregando los caracteres.
    cypher = ""

    # Loopear por la string
    for i in texto:
        # Devuelve la letra si esta en ABC_REAL (es mayus); si es minuscula devuelve la letra pero en mayus, si no es una letra devuelve None
        letter_to_look = i if i in ABC_REAL else chr(ord(i) - 32) if i.isalpha() else None

        # Si no es una letra, lo agrega como el caracter que ya era.
        if not letter_to_look:
            cypher += i
            continue
        
        # Buscar el indice de la letra en el abecedario real
        posicion = ABC_REAL.index(letter_to_look)

        # Agregar a la string final la letra mayuscula o minuscula fijandose como era previo a la conversion de letter_to_look
        cypher += KEY[posicion] if i in ABC_REAL else chr(ord(KEY[posicion]) + 32)
    
    # Cuando termina, devuelve el texto cifrado
    return cypher

if __name__ == "__main__":
    texto = input("Ingrese el texto a cifrar: ")        # Tomar texto...
    print(CifrarConClave(texto))                        # Llamar a la función...
