# 
# GitHub: @GianK128
#

import re as regex
import unicodedata

# Esto requiere explicación...
# Los carácteres con acento u otros diacriticos son combinaciones de caracteres Unicode. 
# Los diacriticos se encuentran en el rango de u0300 a u036f. Queremos conservar el '~' (u0303) ya que se utiliza para la 'ñ'.
# Con la libreria unicodedata, podemos convertir el texto a NFD (Normalization Form Decomposition).
# El texto normal esta en NFC, al convertirlo a NFD, las letras y los diacríticos se separan y se colocan en secuencia.
# Entonces podemos analizar la siguiente regex:
# ([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+
#
#   - ([^n\u0300-\u036f])[\u0300-\u036f]+
#       - [^n\u0300-\u036f] chequea los caracteres que comiencen con una 'n' y les siga un diacritico.
#       - [\u0300-\u036f] chequea por diacriticos.
#       - La secuencia chequea por una o mas ocurrencias de caracteres que sean una 'n' y le sigan dos diacriticos.
#   
#   - n(?!\u0303(?![\u0300-\u036f]))[\u0300-\u036f]+
#       - n(?!\u0303(?![\u0300-\u036f])) chequea los caracteres que sean una 'n' que no esten seguidos de una '~', siempre y cuando no esten seguidos de otro diacritico.
#       - [\u0300-\u036f] chequea por diacriticos.
#       - La secuencia chequea por letras 'n' que no sean una 'ñ', y solo las elimina si lo sigue otro diacritico (ej. 'n~~').
#
#   La secuencia final con las dos busquedas de 'n' con diacriticos puestas en OR (|) basicamente busca por una o mas ocurrencias donde haya un diacritico o donde haya diacriticos que no formen una 'ñ'.
#
# Referencia: https://es.stackoverflow.com/questions/135707/cómo-puedo-reemplazar-las-letras-con-tildes-por-las-mismas-sin-tilde-pero-no-l.

re_acento_match = r'([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+'

def clean_string(txt: str) -> str:
    """
        Limpia la string quitandole los acentos y simbolos (dejando las letras 'Ñ').

        `txt`: str a transformar.

        Devuelve:
        `str`: la str transformada.
    """
    # Acá hacemos la busqueda por regex y lo reemplazamos por el primer caracter en la ocurrencia (que siempre sería una letra).
    # Le entregamos la string normalizada a NFD para hacer la busqueda, le pasamos la flag I para que haga una busqueda 'case-insensitive'.
    # Luego, la volvemos a normalizar a NFC.
    new_s = regex.sub(re_acento_match, r'\1', unicodedata.normalize("NFD", txt), 0, regex.I)
    new_s = unicodedata.normalize("NFC", new_s)

    # Acá buscamos todas las ocurrencias de caracteres que sean alfanumericos y las juntamos (asi queda sin espacios).
    new_s = ''.join(regex.findall("\w+", new_s))
    
    # La devolvemos en minuscula.
    return new_s.lower()

def is_palindrome(txt: str) -> str:
    """
        Chequea si una str es un palindromo.

        `txt`: str a analizar.

        Devuelve:
        `str`: una str diciendo si es un palindromo o no.
    """
    # Limpiar la string primero.
    clean = clean_string(txt)
    
    # Sacar donde está la mitad del texto.
    half_index = (len(clean) - 1) // 2

    # Corregir donde separamos el texto para evitar errores
    if len(clean) % 2 == 0:
        corrector = 1
    else:
        corrector = 0

    # Devolver texto adecuado a si la primera mitad es igual a la segunda mitad en reversa.
    return "¡El texto es palindromo!" if (clean[:half_index + corrector:] == clean[:half_index:-1]) else "¡El texto no es palindromo!"

if __name__ == "__main__":
    while True:
        s = input("Ingrese una oración para ver si es un palindromo.")
        print(is_palindrome(s))
