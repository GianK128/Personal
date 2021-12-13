# 
# GitHub: @GianK128
#

import os
import csv

# Obtener la carpeta donde se encuentra el archivo
curr_dir = os.path.dirname(os.path.realpath(__file__))

# Generar direccion del archivo
cc_filepath = f"{curr_dir}/data"

# Lista de condiciones para cada red bancaria
# [0] son los numeros con los que comienza
# [1::] son los largos posibles del numero
CC_CONDITIONS = {
    "VISA" : ["4", 13, 16],
    "MASTERCARD" : [("51", "52", "53", "54", "55"), 16],
    "AMERICAN EXPRESS" : [("34", "37"), 15]
}

def validate_cc(number: str) -> bool:
    """
        Validar número de tarjeta de crédito usando el algoritmo de Luhn.

        `number`: string con el numero de tarjeta.

        Devuelve:
        `bool`: si el número es válido o no.
    """
    # Multiplicar por 2 cada 2 numeros empezando por el penultimo, luego unirlo en una str
    first = ''.join([str(int(i)*2) for i in number[-2::-2]])

    # Sumar los "digitos", que ya se encuentran unidos en la str
    second = sum(int(i) for i in first)

    # Sumar los numeros que no estuvieron en el primer paso
    final = sum(int(i) for i in number[::-2]) + second

    # Devolver si es divisible por 10 o no.
    return (final % 10 == 0)

def identify_cc(number: str) -> str:
    """
        Identificar a que red bancaria pertenece una tarjeta.

        `number`: string con el numero de tarjeta.

        Devuelve:
        `str`: el nombre de la red bancaria segun `CC_CONDITIONS`.
    """
    # Ciclar para cada condicion
    for red, cond in CC_CONDITIONS.items():
        # Si no empieza por lo correspondiente, pasar al siguiente ciclo
        if not number.startswith(cond[0]):
            continue

        # Ciclar por los largos posibles y si se cumple devolver el nombre de la red
        for largo_posible in cond[1::]:
            if len(number) == largo_posible:
                return red

    # Si no se cumple ninguna condicion, devolver esto
    return "INVALIDA"

def validate_cc_csv():
    # Aca metemos las nuevas filas para el archivo
    new_rows = []

    # Abrir archivo y crear un reader
    with open(f"{cc_filepath}/tarjetas.csv") as f:
        reader = csv.DictReader(f)

        # Pasar por el reader, obtener el numero de tarjeta
        for row in reader:
            cc_num = row['TARJETA']

            # Si no es valida por Luhn, agregarla como invalida.
            if not validate_cc(cc_num):
                new_rows.append({'TARJETA': cc_num, 'RED': "INVALIDA"})
                continue

            # Si es valida, agregarla segun su red o si no pertenece a ninguna.
            new_rows.append({'TARJETA': cc_num, 'RED': identify_cc(cc_num)})
        
        # Abrir nuevo archivo csv y meterle los datos luego de la validacion
        with open(f"{cc_filepath}/identified_tarjetas.csv", "w", newline='') as nf:
            writer = csv.DictWriter(nf, ['TARJETA', 'RED'])

            writer.writeheader()
            writer.writerows(new_rows)

if __name__ == "__main__":
    validate_cc_csv()
