#Proyecto Nº 1: Mad Libs Simple (24/08/2020)
#   -Obtiene input del usuario y lo ingresa en una 'carta' ya predeterminada
#
#   *PRACTICA DE: Input del usuario y manejo de strings
#   *TIEMPO DE REALIZACION: < 15min

def WaitForInput():
    sustantivo1 = input("Sustantivo:" )
    sustantivo2 = input("Sustantivo:" )
    adjetivo1 = input("Adjetivo:" )
    adjetivo2 = input("Adjetivo:" )
    print('\nMadLib:\nHola {}, soy {}, soy un poco {} y {}. Gusto en conocerte.'.format(sustantivo1, sustantivo2, adjetivo1, adjetivo2))

#=====MAIN=====#
if __name__ == "__main__":
    WaitForInput()
        