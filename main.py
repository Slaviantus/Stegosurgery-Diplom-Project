#from kivy.app import App
from kivy.config import Config

Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '850')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from tkinter import Tk
from tkinter import filedialog

from Surgeon import Surgeon
import math


#_______ Surgeon - the manager of all processes in app ___________
#        and provides connection between GUI and classes in app
surgeon = Surgeon()
#_________________________________________________________________







class StartWindow(Screen):

    def load_file(self):
        Tk().withdraw()
        file_path = filedialog.askopenfilename(title = "Open document", filetypes = (("MS Word documents","*.docx"),))

        if (file_path != ''):

            self.__path = file_path
            self.file_path_label.text = file_path
            self.choose_way.text = "Choose the operation with document"
            self.embedding_button.disabled = False
            self.embedding_button.text = "Embedding"
            self.decoding_button.disabled = False
            self.decoding_button.text = "Decoding"

            surgeon.Load_Document(self.__path)



class AutopsyWindow(Screen):

    def on_open_window(self):

        surgeon.Autopse_Document()
        self.complete_label.text = "Autopsy is complete"
        self.loading_label.text = ""
        self.next_button.text = "Next"
        self.next_button.disabled = False

    def on_close_window(self):

        self.complete_label.text = ""
        self.next_button.text = ""
        self.next_button.disabled = True
        self.loading_label.text = "Loading..."





class SettingsWindow(Screen):

    def choose_enc_language(self, instance, value, encoding):

        if value == True:

            if encoding == "ASCII":
                surgeon.LSB_method.Encoding = "ASCII"
            else:
                surgeon.LSB_method.Encoding = "Unicode"


    def choose_bits_number(self, instance, value, bits):

        if value == True:

            if bits == 1:
                surgeon.LSB_method.Last_bits = 1
            elif bits == 2:
                surgeon.LSB_method.Last_bits = 2
            else:
                surgeon.LSB_method.Last_bits = 3


    def spray_mode(self, instance, value):

        if value == True:

            self.key_description.text = "The root of key should be irrational fraction \n also key can be word \"pi\" or \"e\""
            self.key_enter.text = "Enter the key:"
            self.key_text.disabled = False
            self.warning_text.text = "Remember that key for decoding!"

            surgeon.Is_spray_active = True
            self.__block_next_button()

        else:

            self.key_description.text = ""
            self.key_enter.text = ""
            self.key_text.disabled = True
            self.key_text.text = ""
            self.warning_text.text = ""

            surgeon.Is_spray_active = False
            self.__unblock_next_button()



    def key_check(self):

        key = self.key_text.text
        go_next = False

        if key.isdigit():

            key = math.sqrt(float(key))

            if (key - int(key) != 0) and key > 0:

                surgeon.spray.key = key
                go_next = True

            else:
                go_next = False

        else:

            if key == "pi":

                surgeon.spray.key = math.pi
                go_next = True

            elif key == "e":

                surgeon.spray.key = math.e
                go_next = True

            else:
                go_next = False

        if go_next:
            self.__unblock_next_button()

        else:
            self.__block_next_button()


    def __block_next_button(self):

        self.next_button.disabled = True
        self.next_button.text = ""


    def __unblock_next_button(self):

        self.next_button.disabled = False
        self.next_button.text = "Next"






class EmbeddingWindow(Screen):

    def on_open_window(self):

        self.available_sym.text = str(surgeon.Available_LSB_symbols)
        self.__show_settings_information()


    def __show_settings_information(self):

        enc_value = surgeon.LSB_method.Encoding.name
        bits_value = surgeon.LSB_method.Last_bits.value

        if enc_value == "ASCII":

            self.enc_information.text = "Encoding = ASCII, text should be only in English"

        else:

            self.enc_information.text = "Encoding = Unicode, you can use any language"

        if bits_value == 3:

            self.bits_information.text = "last bits of one color channel = 1"

        elif bits_value == 6:

            self.bits_information.text = "last bits of one color channel = 2"

        else:

            self.bits_information.text = "last bits of one color channel = 3"



    def text_calc(self):
        """Calculates the length of message"""

        self.message_len.text = str(len(self.text_input.text))


    def on_next_button(self):
        surgeon.Secret_message = self.text_input.text





class ImplementationWindow(Screen):

    def on_open_window(self):

        mes_length = len(surgeon.Secret_message)
        char_limit = surgeon.Available_LSB_symbols

        if mes_length > char_limit:

            self.top_text_a.text = "WARNING"
            self.top_text_b.text = "The number of characters exceeds the limit"
            self.start_button.disabled = True
            self.start_button.text = ""
            self.spread_mes.text = ""
            self.spread_check.disabled = True
            self.spread_check.opacity = 0
            self.spread_check.active = False

        else:

            self.top_text_a.text = "The secret message is ready"
            self.start_button.disabled = False
            self.start_button.text = "Start Embedding"
            self.spread_mes.text = ""
            self.spread_check.disabled = True
            self.spread_check.opacity = 0
            self.spread_check.active = False

        if mes_length * 2 <= char_limit:

            self.top_text_a.text = "Your message is short"
            self.top_text_b.text = "You can spread it to all document"
            self.spread_mes.text = "Spread message"
            self.spread_check.disabled = False
            self.spread_check.opacity = 1


    def on_embedding_button(self):

        if self.spread_check.active == True:

            surgeon.LSB_method.diffuse = True

        else:

            surgeon.LSB_method.diffuse = False





class StitchingWindow(Screen):

    def on_open_window(self):

        surgeon.Use_LSB_method()
        #_____ FOR LOGGING DOCUMENT _____
        #surgeon.Log_Doc()
        #________________________________
        message = surgeon.LSB_decode_document()
        self.check_dec_text.text = message


    def Save_file(self):

        Tk().withdraw()
        file_path = filedialog.asksaveasfilename(title = "Save document", filetypes = (("MS Word documents","*.docx"),))
        docx_extent = '.docx'
        file_path = file_path + docx_extent
        surgeon.Save_Document(file_path)

    def on_close_window(self):

        self.check_dec_text.text = ""



class Decoding_Settings_Window(Screen):

    def on_open_window(self):

        if surgeon.Has_document_something():

            self.empty_doc_label.text = ""
            self.dec_anyway_label.text = ""
            self.dec_anyway.disabled = True
            self.dec_anyway.opacity = 0
            self.__block_decoding_settings()

        else:

            self.empty_doc_label.text = "The Document is empty!"
            self.dec_anyway_label.text = "Decode it anyway"
            self.dec_anyway.disabled = False
            self.dec_anyway.opacity = 1
            self.__block_decoding_settings()


    def manual_decoding(self, instance, value):

        if value == True:
            self.__unblock_decoding_settings()

        else:
            self.__block_decoding_settings()



    def choose_decoding_way(self, instance, value, decoding_way):

        if value == True:

            if decoding_way == "Classic":

                surgeon.Is_spray_active = False

                self.__unblock_decode_button()
                self.__block_enter_key()

            else:

                surgeon.Is_spray_active = True

                self.__block_decode_button()
                self.__unblock_enter_key()


    def key_check(self):

        key = self.key_text.text
        go_next = False

        if key.isdigit():

            key = math.sqrt(float(key))

            if (key - int(key) != 0) and key > 0:

                surgeon.spray.key = key
                go_next = True

            else:
                go_next = False

        else:

            if key == "pi":

                surgeon.spray.key = math.pi
                go_next = True

            elif key == "e":

                surgeon.spray.key = math.e
                go_next = True

            else:
                go_next = False

        if go_next:
            self.__unblock_decode_button()

        else:
            self.__block_decode_button()


    def choose_enc_language(self, instance, value, encoding):

        if value == True:

            if encoding == "ASCII":
                surgeon.LSB_method.Encoding = "ASCII"
            else:
                surgeon.LSB_method.Encoding = "Unicode"


    def choose_bits_number(self, instance, value, bits):

        if value == True:

            if bits == 1:
                surgeon.LSB_method.Last_bits = 1
            elif bits == 2:
                surgeon.LSB_method.Last_bits = 2
            else:
                surgeon.LSB_method.Last_bits = 3





    def __block_decode_button(self):

        self.decode_button.disabled = True
        self.decode_button.text = ""

    def __unblock_decode_button(self):

        self.decode_button.disabled = False
        self.decode_button.text = "Decode"

    def __block_enter_key(self):

        self.key_enter.text = ""
        self.key_text.disabled = True

    def __unblock_enter_key(self):

        self.key_enter.text = "Enter the key"
        self.key_text.disabled = False

    def __block_decoding_settings(self):

        self.ascii_label.text = ""
        self.ascii_check_box.disabled = True
        self.ascii_check_box.opacity = 0

        self.unicode_label.text = ""
        self.unicode_check_box.disabled = True
        self.unicode_check_box.opacity = 0

        self.bit1_label.text = ""
        self.bit1_check_box.disabled = True
        self.bit1_check_box.opacity = 0

        self.bit2_label.text = ""
        self.bit2_check_box.disabled = True
        self.bit2_check_box.opacity = 0

        self.bit3_label.text = ""
        self.bit3_check_box.disabled = True
        self.bit3_check_box.opacity = 0


    def __unblock_decoding_settings(self):

        self.ascii_label.text = "ASCII (english) 1 symbol = 8 bits"
        self.ascii_check_box.disabled = False
        self.ascii_check_box.opacity = 1

        self.unicode_label.text = "Unicode (any) 1 symbol = 16 bits"
        self.unicode_check_box.disabled = False
        self.unicode_check_box.opacity = 1

        self.bit1_label.text = "1 bit"
        self.bit1_check_box.disabled = False
        self.bit1_check_box.opacity = 1

        self.bit2_label.text = "2 bits"
        self.bit2_check_box.disabled = False
        self.bit2_check_box.opacity = 1

        self.bit3_label.text = "3 bits"
        self.bit3_check_box.disabled = False
        self.bit3_check_box.opacity = 1




class DecodingWindow(Screen):

    def on_open_window(self):

        message = surgeon.LSB_decode_document()
        self.decoded_text_table.text = message


    def on_close_window(self):

        self.decoded_text_table.text = ""











class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("stegosurgery.kv")


class StegosurgeryApp(App):
    def build(self):

        return kv


if __name__ == "__main__":
    StegosurgeryApp().run()

