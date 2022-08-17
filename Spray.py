import random
import math
from DataConverter import DataConverter

class Spray:

    def __init__(self):

        self.__key = str(math.pi%1)  #default key value
        self.__converter = DataConverter()


    @property
    def key(self) -> float:

        return self.__key


    @key.setter
    def key(self, key: float):

        key = str(key%1)
        str_key = list()

        for i in range(2, len(key)):
            if key[i] == "0":
                str_key.append("1")

            else:
                str_key.append(key[i])

        self.__key = self.__converter.ListToString(str_key)  #key should be irrational fraction




    def Sprayed_bit_size(self, container_bit_size: int) -> int:
        """Calculates the number of bits for message with using spraying"""

        key = self.__key

        i = 0
        key_index = 2
        bit_size = 0

        while i <= container_bit_size:

            if key_index == len(key):
                key_index = 2

            i += int(key[key_index])

            if int(key[key_index]) != 0 and i <= container_bit_size:
                bit_size += 1

            key_index += 1

        return bit_size



    def Spray_Message(self, bin_message: str, container_bit_size: int):
        """Spraying the binary secret message according to key with adding noise"""

        key = self.__key
        sprayed_message = list()

        key_index = 0
        mes_index = 0
        spray_index = int(key[key_index])

        for i in range(0, container_bit_size):

            if i == spray_index and mes_index < len(bin_message):

                sprayed_message.append(bin_message[mes_index])

                key_index += 1

                if key_index == len(key):
                    key_index = 0

                spray_index += int(key[key_index])
                mes_index += 1

            else:
                sprayed_message.append(str(random.randint(0, 1)))


        return self.__converter.ListToString(sprayed_message)



    def Decode_Sprayed_Message(self, sprayed_message: str) -> str:
        """extraction secret binary message according to key from noise"""

        key = self.__key
        bin_message = list()

        key_index = 0
        spray_index = int(key[key_index])

        for i in range(0, len(sprayed_message)):

            if i == spray_index:

                bin_message.append(sprayed_message[i])

                key_index += 1

                if key_index == len(key):
                    key_index = 0

                spray_index += int(key[key_index])


        return self.__converter.ListToString(bin_message)