import os
import shutil
import getpass
import string
import random
from Crypto.Cipher import AES

def generate_key():
    # Rastgele bir anahtar oluşturur
    characters = string.ascii_letters + string.digits + string.punctuation
    key = ''.join(random.choice(characters) for _ in range(16))
    return key.encode()

def encrypt_file(file_path, key):
    # Dosyayı şifreler
    cipher = AES.new(key, AES.MODE_EAX)
    with open(file_path, 'rb') as file:
        plaintext = file.read()
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    
    # Şifrelenmiş veriyi yeni bir dosyaya yazar
    encrypted_file_path = file_path + '.enc'
    with open(encrypted_file_path, 'wb') as encrypted_file:
        [encrypted_file.write(x) for x in (cipher.nonce, tag, ciphertext)]
    
    # Orijinal dosyayı siler
    os.remove(file_path)
    
    return encrypted_file_path

def decrypt_file(encrypted_file_path, key):
    # Şifrelenmiş dosyayı açar
    with open(encrypted_file_path, 'rb') as encrypted_file:
        nonce, tag, ciphertext = [encrypted_file.read(x) for x in (16, 16, -1)]
    
    # Dosyayı şifre çözer
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    
    # Şifresi çözülmüş veriyi yeni bir dosyaya yazar
    decrypted_file_path = encrypted_file_path[:-4]
    with open(decrypted_file_path, 'wb') as decrypted_file:
        decrypted_file.write(plaintext)
    
    # Şifrelenmiş dosyayı siler
    os.remove(encrypted_file_path)
    
    return decrypted_file_path

def main():
    file_path = input("Şifrelemek istediğiniz dosyanın yolunu girin: ")
    key = generate_key()
    
    # Dosyayı şifreler
    encrypted_file_path = encrypt_file(file_path, key)
    print("Dosya şifrelendi:", encrypted_file_path)
    
    # USB bellek takılıp çıkarılmasını bekler
    while True:
        usb_drive = input("USB bellek takıldı mı? (E/H): ")
        if usb_drive.upper() == 'E':
            break
    
    # Dosyayı geri çözer
    decrypted_file_path = decrypt_file(encrypted_file_path, key)
    print("Dosya geri çözüldü:", decrypted_file_path)

if __name__ == "__main__":
    main()
