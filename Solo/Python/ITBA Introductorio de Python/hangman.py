# KEBERLEIN, Gian Franco - 17/05/2021, 02:34 AM
# Desafio numero 2 del curso introductorio de python de IEEE - ITBA
# Juego de ahorcado

def HangmanPlay(word: str, tries: int) -> int:
    try_number = 0
    errores = 0
    to_guess = word

    while True:
        # Chequear si se paso de intentos posibles
        if errores > tries:
            return 0

        # Pedir una letra o palabra
        guess = input()
        
        # Si esta vacia la entrada reiniciar el loop
        if guess == "":
            continue

        # Si es una palabra ver si es la palabra que se desea, sino reintentar
        if len(guess) > 1:
            if guess.upper() == word:
                return try_number
            else:
                try_number += 1
                errores += 1
                continue
        
        # Ver si la letra está en la palabra a buscar, quitarla de la palabra y pasar al siguiente intento.
        if guess.upper() in to_guess:
            to_guess = to_guess.replace(guess.upper(), "")
        else:
            try_number += 1
            errores += 1
            continue
        
        try_number += 1

        # Si la palabra ya esta vacia, entonces devolver numero de intentos.
        if not to_guess:
            return try_number

# Preguntar por palabra e intentos
string = input()
tries = int(input())

# Llamar al juego
p = HangmanPlay(string.upper(), tries)
print(p)