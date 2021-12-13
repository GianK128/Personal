# 
# GitHub: @GianK128
#

from random import shuffle

class Encrypter():
    __instance_num = 1
    __abc_real = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZabcdefghijklmnñopqrstuvwxyz"
    
    def __init__(self, key: str = None):
        """
            Clase con capacidades para cifrar o descifrar textos usando una KEY otorgada.

            Si no se le otorga ninguna, generará una aleatoria.

            `key`: una string con la key a utilizar. Deben ser solo letras y todas en mayúsculas.
            Tambien debe tener la letra Ñ asi que debe ser de longitud 27.
        """
        self.instance_num = Encrypter.__instance_num
        Encrypter.__instance_num += 1

        if not key:
            self.__key = self.generate_random_key()
        else:
            self.__key = self.validate_key(key)
        
    def Cifrar(self, txt: str, times: int) -> str:
        """
            Método para cifrar una string `times` veces usando la `KEY` otorgada en el constructor.
        
            Devuelve:
            `str`: el texto cifrado.
        """
        trans_table = str.maketrans(self.__abc_real, self.__key)
        translated = txt
        for i in range(times):
            translated = translated.translate(trans_table)
        return translated

    def Descifrar(self, txt: str, times: int) -> str:
        """
            Método para descifrar una string `times` veces usando la `KEY` otorgada en el constructor.
        
            Devuelve:
            `str`: el texto descifrado.
        """
        trans_table = str.maketrans(self.__key, self.__abc_real)
        translated = txt
        for i in range(times):
            translated = translated.translate(trans_table)
        return translated
                
    @property
    def InstanceNumber(self):
        """
            El numero de instancia creada de Encrypter desde que empezó el programa.
        """
        return self.instance_num

    @property
    def KEY(self):
        """
            La clave utilizada para cifrar/descrifrar los textos.
        """
        return self.__key

    @KEY.setter
    def KEY(self, new_key):
        self.__key = self.validate_key(new_key)

    @staticmethod
    def generate_random_key() -> str:
        """
            Genera una key aleatoria mezclando el abecedario.
            
            La key generada tiene la letra Ñ, por lo tanto es de longitud 27.
        """
        abc = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'
        abc_list = []

        for c in abc:
            abc_list.append(c)

        shuffle(abc_list)
        key = "".join(abc_list)

        return key + key.lower()

    def validate_key(self, key: str) -> str:
        """
            Chequear si una `KEY` otorgada es valida o no (longitud correcta y si son puras letras).

            Si es invalida, imprime un mensaje y luego genera y devuelve una `KEY` aleatoria.

            Si es valida, devuelve la `KEY` otorgada.
        """
        if len(set(key)) == 54 and key.isalpha():
            return key
        elif len(set(key)) != 27 or not key.isalpha():
            print(f"La KEY para {self} es invalida. Generando una aleatoria...")
            return self.generate_random_key()
        else:
            return key + key.lower()
    
    def RegenerarKey(self) -> str:
        """
            Generar una nueva `KEY` aleatoria y asignarsela a este objeto de Encrypter.
        """
        self.__key = self.generate_random_key()

    def __repr__(self) -> str:
        return "Encrypter Nº" + str(self.instance_num)

if __name__ == "__main__":
    test = Encrypter("KHTRDWFOALYSCXEIUJQÑZGNPVMB")

    print(test.Cifrar("Hello World!", 3))
    print(test.Descifrar("Aqeek Gklej!", 3))
