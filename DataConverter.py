from docx import Document
from docx.shared import RGBColor


class DataConverter:

    def StringToBin(self, message: str) -> list:
        """Convert from string to binary code"""

        binMessage = list(range(0, len(message)))
        for i in range(0, len(message)):
            binMessage[i] = format(ord(message[i]), 'b')

        return binMessage


    def BinToString(self, message: list) -> list:
        """Convert from binary code to string"""

        _str_list = list(range(0, len(message)))
        for i in range(0, len(message)):
            _decimal = int(message[i], 2)
            _str_list[i] = chr(_decimal)
        #print(''.join(_str_list))
        return _str_list


    def ListToString(self, message: list) -> str:
        """Convert from list of characters to string"""
        return ''.join(message)


    def RGBtoBin(self, color: RGBColor) -> str:
        """Convert from RGBColor to binary string of color"""
        hex_color = color.__str__()
        bin_length = len(hex_color) * 4
        hex_as_int = int(hex_color, 16)
        hex_as_binary = bin(hex_as_int)
        padded_binary = hex_as_binary[2:].zfill(bin_length)
        return padded_binary


    def BinToRGB (self, binColor: str) -> RGBColor:
        """Convert from binary color string to RGBColor"""
        redDecimal = int(binColor[0:8], 2)
        greenDecimal = int(binColor[8:16], 2)
        blueDecimal = int(binColor[16:24], 2)

        charColor = RGBColor(redDecimal, greenDecimal, blueDecimal)

        return charColor


    def AllTo8bit (self, bin_message: list) -> list:
        """Transform all bin characters to 8 bit"""

        for i in range(0, len(bin_message)):
            num_bits = len(bin_message[i])
            if num_bits < 8:
                difference = 8 - num_bits
                bin_message[i] = '0' * difference + bin_message[i]

        return bin_message


    def AllTo16bit(self, bin_message: list) -> list:
        """Transform all bin characters to 16 bit"""

        for i in range(0, len(bin_message)):
            num_bits = len(bin_message[i])
            if num_bits < 16:
                difference = 16 - num_bits
                bin_message[i] = '0' * difference + bin_message[i]

        return bin_message


