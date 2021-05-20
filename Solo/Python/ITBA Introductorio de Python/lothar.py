# KEBERLEIN, Gian Franco - 12/05/2021
# Ultimo editado: 17/05/2021, 02:46 AM
# Desafio numero 1 del curso introductorio de python de IEEE - ITBA

# Funcion lothar => si el numero es par lo divide por dos, si es impar lo multiplica por 3 y le suma 1.
# Devuelve el numero de intentos que le tomo hasta llegar a 1.

def lothar(n, step = 0):
    # if n <= 1:
    #     return step
    # if n % 2 == 0:
    #     return lothar(n / 2, step + 1)
    # else:
    #     return lothar((n * 3) + 1, step + 1)

    # One Liner
    return step if n <= 1 else lothar(n/2, step + 1) if n % 2 == 0 else lothar(n*3 + 1, step + 1)

if __name__ == "__main__":
    n = int(input())

    result = lothar(n)
    print(result)