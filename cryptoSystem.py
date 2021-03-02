import os
from cryptography.fernet import Fernet
import string
import numpy as np
from sympy import Matrix
import binascii
import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

#MENU
def menu():

    print("[+] Bienvenido/a al cifrador HEA, ¿Que desea realizar? \n")

    print("[1] Encriptar un archivo con clave simetrica")
    print("[2] Desencriptar un archivo con clave simetrica")
    print("[3] Encriptar un archivo con clave asimetrica")
    print("[4] Desencriptar un archivo con clave asimetrica")
    print("[5] Encriptar un archivo con cifrado por matrices")
    print("[6] Desencriptar un archivo con cifrado por matrices")

    print("[0] Salir del sistema \n")

##ENCRIPTACION SIMETRICA##

def write_key(key):
    with open("keyfile.key", "wb") as file:
        file.write(key)
        
def load_key():
    with open ("keyfile.key", "rb") as file:
        return file.read()

#CIFRADO
def encrypt_file(filename,key):
    f = Fernet(key)
    encrypted = b''

    with open(filename, "rb") as file:
        data = file.read()
        encrypted = f.encrypt(data)
    
    with open(filename, "wb") as file:
        file.write(encrypted)

#DESCIFRADO
def decrypt_file(filename,key):
    f = Fernet(key)
    encrypted_data = b''

    with open (filename, "rb") as file:
        encrypted_data = file.read()

    decrypted_data = f.decrypt(encrypted_data)

    with open (filename, "wb") as file:
        file.write(decrypted_data)
   

##ENCRIPTACION POR MATRICES##

def preprocessing(m):
    m = m.replace(" ","").replace(",","").replace(".","").replace("'","").replace(":","").replace(";","")
    m = m.lower()
    return m

def lettersOfPlaintext(m):
    letters = []
    for i in range(0, len(m)):
        letters.append(m[i])
    return letters

def letterToNumber(letter):
    return string.ascii_lowercase.index(letter)

def numberToLetter(number):
    return chr(int(number) + 97)

def module(letter_index):
    
    while(letter_index < 0):
        letter_index += 26
       
    while(letter_index > 25):
        letter_index -= 26
    
    return letter_index



menu()
option = int(input("[+] Introduzca la seleccion: "))

while option != 0:

    if option == 1:
        key = Fernet.generate_key()
        write_key(key)
        filename = input("[+] Introduzca el nombre del archivo que desea encriptar: ")
        
        encrypt_file(filename,key)

        print("[+] El archivo fue encriptado con exito")
        input("[+] Presione enter para continuar...")
        pass

    elif option ==2:
        
        filename = input("[+] Introduzca el nombre del archivo que desea desencriptar: ")
        key = load_key()

        decrypt_file(filename,key)

        print("[+] El archivo fue desencriptado con exito")
        input("[+] Presione enter para continuar...")

        pass
        
    elif option == 3:

        random_generator = Crypto.Random.new().read

        private_key = RSA.generate(2048, random_generator)
        public_key = private_key.publickey()



        #CREAR ARCHIVO DE LLAVE PRIVADA
        private_key = private_key.exportKey("PEM")

        with open ("PrivateKey.pem", "wb") as pfile:
            pfile.write(private_key)

        private_key = RSA.importKey(open("PrivateKey.pem", "rb").read())


        #CREAR ARCHIVO DE LLAVE PUBLICA
        public_key = public_key.exportKey("PEM")

        with open ("PublicKey.pem", "wb") as pfile:
            pfile.write(public_key)

        public_key = RSA.importKey(open("PublicKey.pem", "rb").read())    

        #ENCRIPTACION
        filename = input("[+] Introduzca el nombre del archivo que desea encriptar: ")
        
        with open (filename, "rb") as file:
            info = file.read()

        message = info

        cipher = PKCS1_OAEP.new(public_key)
        encryptmessage = cipher.encrypt(message)

        with open (filename, "wb") as file:
            file.write(encryptmessage)

        print("[+] El archivo fue encriptado con exito")
        input("[+] Presione enter para continuar...")

        pass

    elif option == 4:


        filename = input("[+] Introduzca el nombre del archivo que desea desencriptar: ")

        with open (filename, "rb") as file:
            encrypinfo = file.read()

        cipher = PKCS1_OAEP.new(private_key)
        message = cipher.decrypt(encrypinfo)

        with open (filename, "wb") as file:
            file.write(message)

        print("[+] El archivo fue desencriptado con exito")
        input("[+] Presione enter para continuar...")


        pass

    elif option == 5:
        
        key = np.array([
        [3, 10, 20],
        [20, 9, 17],
        [0, 4, 17],
        ])

        key.shape[0] == key.shape[1]
        np.linalg.det(key) !=0
        m = input("[+] Introduzca el texto a encriptar :")
        m = preprocessing(m)
        plaintext = lettersOfPlaintext(m)
        plaintext_idx = []

        for i in plaintext:
            plaintext_idx.append((letterToNumber(i)))

        plaintext_matrix = np.array(plaintext_idx)
        plaintext_matrix.resize(5,3)

        #Encryption
        encryption = np.matmul(plaintext_matrix, key) % 26
        encryption.resize(1,15)
        ciphertext = []
        for i in encryption.tolist()[0]:
            ciphertext.append(numberToLetter(i))
        
        print(ciphertext)
        print("[+] El archivo fue encriptado con exito")
        input("[+]Presione enter para continuar...")


        pass

    elif option == 6:
        
        #Decryption
        
        inv_key = Matrix(key).inv_mod(26)
        inv_key = np.array(inv_key)
        inv_key = inv_key.astype(float)

        np.matmul(key, inv_key)%26
        encryption.resize(5, 3)
        decryption = np.matmul(encryption, inv_key) % 26
        decryption.resize(1,15)

        restored_text = []

        for i in decryption.tolist()[0]:
            restored_text.append(numberToLetter(i))

        print(restored_text)
        print("[+] El archivo fue desencriptado con exito")
        input("[+] Presione enter para continuar...")
        

        pass

    else:
        print("Opcion invalida")
        input("[+] Presione enter para continuar...")
    
    os.system("cls")
    menu()
    option = int(input("[+] Introduzca la seleccion: "))

print ("\nGracias por usar nuestro sistema")

