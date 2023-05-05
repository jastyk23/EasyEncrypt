'''
Данный скрипт использует модуль Fernet для шифрования файлов.
Для этого необходима цель и ключ. Если при шифровании ключ отсутствует, то он генерируется автоматически 
и сохраняет в корневой папке. При это ключ скрывается для отображения. Данные по ключу выводятся в консоль.
Для дешифрирования необходим ключ, без него файл расшифровать не получится. 
Скрипт создан для личного пользования.
'''
import os
import platform
import subprocess
import argparse
from sys import argv
try: # Импортирует модуль cryptography, а при необходимости устанавливает его.
    from cryptography.fernet import Fernet
except:
    while True:
        pos = input('Для работы необходимо установить модуль cryptography. Выполнить установку? (Д/Н): ').lower()
        match pos:
            case 'д' | 'да' | 'y' | 'yes':
                mod_inst = subprocess.Popen("pip  install cryptography", shell=True) 
                mod_inst.wait()
                break
            case 'н' | 'нет' | 'n' | 'no' | 'not':
                print('Без модуля работа невозможна.')
                exit()
            case _:
                print('Команда не опознана! Попробуйте еще раз.')
    
    from cryptography.fernet import Fernet

def createParser():
    # Справка и опции скрипта
    parser = argparse.ArgumentParser(
         prog = 'cryptography',
         description = '''Зашакалю нужный файл,
         всё будет круто, смотри справку.''',
         epilog = '''Пример python3 srypt.py -d target=file.txt key=crypto.key\n
         (c) Jasty 2023. Если ключа нет, то расшифровать не получится.\n
         И запомни - если обосрался, назад дороги не будет!''',
         add_help=False
    )
    parser.add_argument ('-h', '--help',action='help', help='Справка')
    parser.add_argument ('-e', '--encrypt', action='store_true', help = 'Шифрует файл, создает скрытый ключ или использует ваш')
    parser.add_argument ('-d', '--decrypt', action='store_true',help = 'Расшифровывает файл, для работы необходимо передать параметр key')
    parser.add_argument('target', nargs='?' ,type=str, help = 'Шифруемый файл')
    parser.add_argument('key', nargs='?', type=str, help = 'Ключ шифрования, если ключа нет при шифровании можно не указывать, он создастся автоматически')
    return parser

def write_key():
    # Создание ключа для шифрования и автоматическое скрытие его в зависимости от ОС
    name = platform.platform()
    key = Fernet.generate_key()
    if 'Linux' in name:
        with open('.crypto.key', 'wb') as key_file:
            key_file.write(key)
        print('Ключ сохранен .crypto.key и скрыт')
    else:
        with open('crypto.key', 'wb') as key_file:
            key_file.write(key)
        subprocess.check_call(["attrib","+H","crypto.key"])
        print('Ключ сохранен crypto.key и скрыт')
    return key

def load_key(key):
    # Загружает ключ
    return open(key, 'rb').read()

def encrypt(filename, key):
    # Шифрование файла
    if key is None:
        key = write_key()
    f = Fernet(key)
    with open(filename, 'rb') as file:
            file_data = file.read()
            encrypted_data = f.encrypt(file_data)

    with open(filename, 'wb') as file:
            file.write(encrypted_data)
    print('Файл зашифрован')
    
def decrypt(filename, key):
    # Дешифрирование файла с помощью ключа.
    if key is None:
        print('Ключ отсутствует')
        exit()
    f = Fernet(key)
    with open(filename, 'rb') as file:
        encrypted_data = file.read()

    decrypted_data = f.decrypt(encrypted_data)
    with open(filename, 'wb') as file:
        file.write(decrypted_data)
    print('Файл расшифрован')

def main():
    parser = createParser()
    namespace = vars(parser.parse_args(argv[1:]))
    crypt = None
    args = {'key': None, 'target': None}
    for name in namespace:
        if name == 'encrypt': # Если encrypt True устанавливает значение crypt True
            if namespace[name]:
                crypt = True
            continue
        elif name == 'decrypt':# Если decrypt True устанавливает значение crypt False
            if namespace[name]:
                crypt = False
            continue
        elif not namespace['decrypt'] and not namespace['encrypt']: # При других значениях - пользователь не выбрал метод работы
            raise ValueError('Модуль не выбран, для просмотра справки используйте -h')
        elif namespace[name] is None:
            continue
        elif 'key' in namespace[name]: # Поиск ключевых аргументов из за особенности их передачи. Пр. namespace = {'encrypt': True, 'decrypt': False, 'target': 'target=try.txt', 'key': 'key=.crypto.key'}
            args['key'] = namespace[name][4:]
        elif 'target' in namespace[name]:
            args['target'] = namespace[name][7:]
        else:
            raise ValueError('Непредвиденная ошибка')


    if args['key']:
        try:
            key = load_key(args['key'])
        except FileNotFoundError:
            raise FileNotFoundError('Ключ отсутсвует')
    else:
        key = None

    if not args['target'] or not os.path.exists(args['target']):
        raise FileNotFoundError('Шифруемая цель отсутствует')
    match crypt:
        case True:
            encrypt(args['target'], key)
        case False:
            decrypt(args['target'], key) 

if __name__ == '__main__':  
    main()
