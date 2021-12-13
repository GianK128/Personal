# 
# GitHub: @GianK128
#

# Lista con posibles billetes.
billetes = [50, 20, 10, 5, 1]

def CalcularBilletes(monto: int) -> dict:
    """
        Devuelve un diccionario donde las keys son el valor de los billetes y los valores son la cantidad.
    """
    # Monto del que se sustrae y el dict de salida.
    new_monto = monto
    newBilletes = {}

    # Ciclar la lista de billetes
    for i in billetes:
        # Sacar la cantidad de billetes necesarios de este tipo
        cant_billetes = int(new_monto / i)

        # Restarle esa cantidad de billetes al monto y agregarlo al dict.
        new_monto -= i * cant_billetes
        newBilletes[i] = cant_billetes
    
    # Devolver el dict con billetes y cantidad
    return newBilletes

if __name__ == "__main__":
    monto = int(input("Monto a retirar: "))
    print(CalcularBilletes(monto))
