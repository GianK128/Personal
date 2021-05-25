def DoubleHalfPyramid(h: int) -> str:
    # Primera solución
    # final_string = ''
    # for i in range(1, h + 1):
    #     final_string += (' ' * (h - i)) + '#' * i + '   ' + '#' * i + '\n'
    # return final_string

    # Segunda solucion con list comprehension
    return ''.join((' ' * (h - i)) + '#' * i + '   ' + '#' * i + '\n' for i in range(1, h + 1))

height = int(input("Height: "))
print(DoubleHalfPyramid(height))