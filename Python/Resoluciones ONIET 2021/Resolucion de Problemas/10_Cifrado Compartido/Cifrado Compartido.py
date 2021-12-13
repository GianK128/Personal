# 
# GitHub: @GianK128
#

# Uso:
# main.py [-c|-d] file.txt (key_qty) (key_times)
import os
from sys import argv
from Encrypter import Encrypter

curr_dir = os.path.dirname(os.path.realpath(__file__))

c_check = argv[1] == '-c' and len(argv) != 5
d_check = argv[1] == '-d' and len(argv) != 3

if c_check or d_check:
    print("Faltan argumentos, o hay de más.")
    exit(1)

param, filename = argv[1], argv[2]

if c_check:
    key_qty, key_times = int(argv[3]), int(argv[4])

def cypher_text(enc: Encrypter, filename: str, key_qty: int, key_times: int):
    enc_data = f"{key_qty}-{key_times}\n"

    with open(filename) as f:
        txt = f.read()
        
        for i in range(key_qty):
            txt = enc.Cifrar(txt, key_times)
            enc_data += f"{enc.KEY}\n"
            enc.RegenerarKey()
        
        enc_data += txt
    
    with open(filename[:-4] + "-C.txt", "w", encoding='utf-8') as f:
        f.write(enc_data)

def descypher_text(enc: Encrypter, filename: str):
    with open(filename, encoding='utf-8') as f:
        enc_list = f.readlines()
    
    key_qty, key_times = enc_list[0].strip().split('-')
    txt = "".join(enc_list[int(key_qty) + 1:])

    for i in range(int(key_qty), 0, -1):
        enc.KEY = enc_list[i].strip()
        txt = enc.Descifrar(txt, int(key_times))

    with open(filename[:-4] + "-D.txt", "w", encoding='utf-8') as f:
        f.write(txt)

if __name__ == "__main__":
    filename = f"{curr_dir}\\data\\{filename}"
    
    if not os.path.isfile(filename):
        print("El archivo no existe.")
        exit(1)

    enc = Encrypter()

    if param == '-c':
        cypher_text(enc, filename, key_qty, key_times)
    elif param == '-d':
        descypher_text(enc, filename)
    else:
        print("Parámetro incorrecto. Use '-c' o '-d'.")
