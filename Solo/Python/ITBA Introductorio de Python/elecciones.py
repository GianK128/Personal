def CalcularGanador(total_votos):
    candidatos = {}
    for i in range(total_votos):
        new_voto = input()

        if new_voto not in candidatos:
            candidatos[new_voto] = 1
        else:
            candidatos[new_voto] += 1

    # Obtener mayor de los elementos por clave del diccionario
    return max(candidatos, key = candidatos.get)

total_votos = int(input())
print(CalcularGanador(total_votos))