# Se tienen billetes de 50, 20, 10, 5 y 1
# Ingreso un monto para retirar
# Calcular cuantos billetes de cada monto te debe dar para tener la menor cantidad de billetes posibles

billetes = [50, 20, 10, 5, 1]

def CalcularBilletes(monto: int) -> dict:
    """
        Devuelve un diccionario donde las keys son el valor de los billetes y los valores son la cantidad.
    """
    new_monto = monto
    newBilletes = {}

    for i in billetes:
        cant_billetes = int(new_monto / i)

        new_monto -= i * cant_billetes
        newBilletes[i] = cant_billetes
    
    return newBilletes

monto = int(input("Monto a retirar: "))
print(CalcularBilletes(monto))