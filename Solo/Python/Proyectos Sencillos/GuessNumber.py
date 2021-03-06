#Proyecto Nº 2: Guess Random Number (26/08/2020)
#   -Se le permite al usuario elegir entre 3 dificultades usando un tipo de switch statement hecho con un dict
#   -Luego de que el usuario intente adivinar el numero, se le dan otras oportunidades, pero presentandole pistas
#   -Las pistas son elegidas desde otro switch hecho con un dict
#   -Si el usuario acierta el numero se lo felicita y se le permite reiniciar o cerrar el programa.
#
#   *PRACTICA DE: Una especie de state machine, variables globales, importar modulos, dicts y funciones varias
#   *TIEMPO DE REALIZACION: 5-15min de planning, 2-3h si se desconocen conceptos, < 1h si se tiene idea de que hacer.
#
#   UPDATE 11/11/2020: Arreglo de algunos fallos. Se agrega 'clamp'

#Modulos
import random

#Variables iniciales
toGuess = 0
hintsMax = 3
hints = hintsMax

#Dificultades:
EASY, MEDIUM, HARD = range(3)

#Tipos de pistas:
BETWEEN, MORETHAN, LESSTHAN, ISEVEN = range(4)

#Funcion clamp
def clamp(value, minval, maxval):
    return max(min(value, maxval), minval)

#Funciones para las pistas
def CheckBetween():
    global toGuess
    global hints
    n1 = clamp(random.randint(toGuess - 10, toGuess), 0, 1000)
    n2 = clamp(random.randint(toGuess, toGuess + 10), 0, 1000)
    print('\nPISTA: El número se encuentra entre {0} inclusive y {1} inclusive. Quedan {2} pistas.'.format(n1, n2, hints - 1))

def CheckMore():
    global toGuess
    global hints
    n = clamp(random.randint(toGuess - 10, toGuess - 1), 0, 1000)
    print('\nPISTA: El número es mayor que {0}. Quedan {1} pistas.'.format(n, hints - 1))

def CheckLess():
    global toGuess
    global hints
    n = clamp(random.randint(toGuess + 1, toGuess + 10), 0, 1000)
    print('\nPISTA: El número es menor que {0}. Quedan {1} pistas.'.format(n, hints - 1))

def CheckEven():
    global toGuess
    global hints
    if toGuess % 2 == 0:
        print('\nPISTA: El número es par. Quedan {0} pistas.'.format(hints - 1))
    else:
        print('\nPISTA: El numero es impar. Quedan {0} pistas.'.format(hints - 1))

#Dict con los tipos de pistas
hintTypes = {
    BETWEEN: CheckBetween,
    MORETHAN: CheckMore,
    LESSTHAN: CheckLess,
    ISEVEN: CheckEven
}

#En caso de elegir correctamente
def CorrectChoice():
    global hints
    hints = hintsMax
    print('¡Adivinaste! Felicidades, ese era el numero que pensaba :)')
    s = input('¿Reiniciar? y/n: ')
    if s == 'y':
        WaitForInput()
    else:
        print('Adiós.')

#En caso de querer tirar una pista
def DropHint():
    global hints
    nHint = random.randint(0, 3)
    typeHint = hintTypes.get(nHint, 0)
    typeHint()
    hints = hints - 1
    guess = input('Adivine nuevamente: ')
    TryGuess(guess)

#En caso de quedarse sin pistas
def TryAgain():
    global hints
    global toGuess
    hints = hintsMax
    print('¡Lastima! No pudiste adivinar el numero :(\nEl número era:', toGuess)
    s = input('¿Reiniciar? y/n: ')
    if s == 'y':
        WaitForInput()
    else:
        print('Adiós.')

#Chequear si se adivino el numero
def TryGuess(number):
    global toGuess
    global hints
    a = int(number)
    if a == toGuess:
        CorrectChoice()
    elif hints > 0:
        DropHint()
    else:
        TryAgain()

#Se elige dificultad facil
def PickEasy():
    global toGuess
    toGuess = random.randint(0, 10)
    guess = input('Intente adivinar el numero, del 0 inclusive al 10 inclusive: ')
    TryGuess(guess)

#Se elige dificultad media
def PickMedium():
    global toGuess
    toGuess = random.randint(0, 100)
    guess = input('Intente adivinar el numero, del 0 inclusive al 100 inclusive: ')
    TryGuess(guess)

#Se elige dificultad dificil
def PickHard():
    global toGuess
    toGuess = random.randint(0, 1000)
    guess = input('Intente adivinar el numero, del 0 inclusive al 1000 inclusive: ')
    TryGuess(guess)

def PickAgain():
    print('\nDificultad no valida. Intente nuevamente.\n')
    WaitForInput()

#Dict con los estados de dificultad
difPick = {
    EASY: PickEasy,
    MEDIUM: PickMedium,
    HARD: PickHard
}

#Metodo para esperar la eleccion de dificultad
def WaitForInput():
    dif = int(input('Elegir dificultad:\n0: Fácil (0-10).\n1: Medio (0-100).\n2: Dificil (0-1000).\n\nEntrada: '))
    CheckInputDif(dif)

#Chequear que dificultad se eligio
def CheckInputDif(arg):
    print('Chequeando entrada...')
    func = difPick.get(arg, PickAgain)
    return func()

#=====MAIN=====#
if __name__ == "__main__":
    WaitForInput()