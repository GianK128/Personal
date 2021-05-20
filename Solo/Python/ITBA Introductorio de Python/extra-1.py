# KEBERLEIN, Gian Franco - 19/05/2021
# Ejercicios integradores extra de la clase 1

# 1:
# Calcula promedio de examenes con diferentes importancias y devuelve si esta aprobado
def promedio(n1, n2, n3):
  general = n1 + n2 + n3
  return ((general * 0.2 + general * 0.5 + general * 0.3) / 3) > 4

# 2:
# Calcular numero de Euler segun formula
def factorial(n):
  return 1 if n <= 1 else n*factorial(n-1)

def calcularEuler(reps = 20):
  num = 1
  for i in range(1, reps + 1):
    num += 1 / factorial(i)
  
  return num

# 3:
# Saber si un numero es primo
def isPrime(n):
    for i in range(2, n**0.5):
        if n % i != 0:
            return False
    return True

# 4:
# Secuencia de Fibonacci
def fib(n):
  if n < 2:
    return n

  final = '0, 1'
  count = 0
  a = 0
  b = 1
  for i in range(0, n):
    final += ', '
    count = a + b
    final += str(count)
    a = b
    b = count

  return final + '.'

# 5:
# Busqueda binaria (para un juego de adivinar)
def guessNumber(low, high):
  while True:
    guess = (low + high) // 2
    print("Computer guessed", guess)

    player = input(">, <, o =: ")
    if player == ">":
      low = guess
    elif player == "<":
      high = guess
    elif player == "=":
      break
    else:
      print("Comando incorrecto")
      continue

  print("La PC acertó el numero.")

# 6:
# Cantidad de fichas de domino de valor maximo 'n'
def CantidadFichas(n):
    sum = 0
    for i in range(n + 1):
        for j in range(i, n + 1):
            sum += 1
    return sum

# Mostrar cada ficha que hay con sus valores
def MostrarFichas(n):
    for i in range(n + 1):
        for j in range(i, n + 1):
            print(f"{i}-{j}")

# Sacar valor maximo de fichas segun la cantidad total
def ValorMaximo(n):
    i = n
    cant = 1
    while i > 0:
        if i - cant > 0:
            i -= cant
            cant += 1
        elif i - cant == 0:
            return cant -1
        else:
            return -1

# 7:
# Definir una funcion que calcule integrales
def f(x):
    return 2*x + 1

def Integral(funcion, borde_a, borde_b, distancia):
    suma_areas = 0
    veces = int((borde_b - borde_a) // distancia)

    for i in range(veces):
        suma_areas += funcion(borde_a + i * distancia) * distancia
    
    return suma_areas

# 8:
# Función que calcula aproximaciones de PI usando una formula
# Por usar recursividad tiene un limite de ciclos que se pueden hacer (funcion factorial de mas arriba)
def CalcularPi(ciclos):
  primera_parte = (2 * (2**0.5)) / 9801
  sumatoria = 0

  for i in range(ciclos + 1):
    sumatoria += (factorial(4*i) * (1103 + (26380 * i))) / (((factorial(i))**4) * (396**(4*i)))

  return 1 / (primera_parte * sumatoria)