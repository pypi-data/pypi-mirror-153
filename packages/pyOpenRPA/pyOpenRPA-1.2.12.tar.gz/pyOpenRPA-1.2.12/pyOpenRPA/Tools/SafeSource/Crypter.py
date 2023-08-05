import os, random, struct
from Crypto.Cipher import AES

def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    """ Шифрует файл используя AES (режим CBC) с
        заданным ключом.

        key:
            Ключ шифрования - строка длиной
            16, 24 или 32 байта. Более длинные ключи
            более безопасны.

        in_filename:
            Имя входного файла

        out_filename:
            Если None, будет использоваться «<in_filename> .enc».

        chunksize:
            Устанавливает размер фрагмента, который функция
            использует для чтения и шифрования файла.Большие
            размеры могут быть быстрее для некоторых файлов и машин. 
            кусок (chunk) должен делиться на 16.
    """
    if not out_filename:
        out_filename = in_filename + '.enc'
    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    iv = iv.encode('utf8')[0:16]
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)
    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)
                outfile.write(encryptor.encrypt(chunk))

def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
    """ Расшифровывает файл, используя AES (режим CBC) с
        заданным ключом. Параметры аналогичны encrypt_file,
        с одним отличием: out_filename, если не указано
        будет in_filename без его последнего расширения
        (т.е. если in_filename будет 'aaa.zip.enc', тогда
        out_filename будет 'aaa.zip')
    """
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]
    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)
        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(origsize)
def decrypt_file_bytes(key, in_filename, chunksize=24*1024):
    """ Расшифровывает файл, используя AES (режим CBC) с
        заданным ключом.
    """
    lResult = b''
    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)
        while True:
            chunk = infile.read(chunksize)
            if len(chunk) == 0:
                break
            lResult = lResult+decryptor.decrypt(chunk)
        lResult=lResult[0:origsize]
    return lResult