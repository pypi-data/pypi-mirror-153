import os

class encode():
    def __init__(self, key=6, disable_key_check=False) -> None:
        if disable_key_check == False:
            if key > 10:
                raise Exception("Key a key higher than 10 might corrupt the data!\nYou can disable this by Typing 'encode(key='Value', disable_key_check=True)'")
        else:
            pass
        
        self.key = key
    
    def encode(self, data):
        output = ""
        for x in range(0, len(data)):
            output += chr(self.key ^ ord(data[x]))
        return output
    
    def help(self):
        print("""
        Usage:
        Thank you for using this tool!
        This tool is a simple tool to encrypt and decrypt data.

        Encrypt:
        encode(data, key='Your key here (number), disable_key_check=(Boolean, True or False)')

        Decrypt:
        encode(data, key='(Same key you wrote when you encoded)', disable_key_check=(Boolean, True or False)')
        """)