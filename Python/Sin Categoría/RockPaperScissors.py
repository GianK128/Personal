#Proyecto Nº 3: Mad Libs Simple (12/03/2021)
#
#   *TIEMPO DE REALIZACION: < 20min

from random import randint

#Listas
moves = ["Rock", "Paper", "Scissors"]   #Movimientos
winningMoves = [-4, 1]                  #Mov. ganadores
losingMoves = [2, -1]                   #Mov. perdedores

#Mov. de la computadora
cpu = randint(1, 3)

#Funcion principal
def Game():
    #Introduccion
    print("Rock, Paper, Scissors!")
    player = int(input("Choose one: (1 - Rock, 2 - Paper, 3 - Scissors)\n"))

    #Limitar entrada
    if player < 0 or player > 4:
        #Número invalido y repetir
        input("Invalid number, please try again.")
        Game()
    else:
        #Calculo para ganar
        num = player - cpu

        #Ver si es ganador o perdedor.
        if num in winningMoves:
            print("You win!")
        elif num in losingMoves:
            print("You lost :(")
        else:
            print("It's a draw.")
        
        #Print final.
        input("Computer picked {0}.\nYou picked {1}.\n".format(moves[cpu - 1], moves[player - 1]))
    
        #Preguntar si quiere jugar otra vez
        i = input("Play Again? y/n\n")
        if i == "y":
            Game()

if __name__ == "__main__":
    Game()