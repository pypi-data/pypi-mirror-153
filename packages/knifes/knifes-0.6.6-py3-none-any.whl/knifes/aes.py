from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import algorithms
from Crypto.Cipher import AES
import base64

'''
AES/CBC/PKCS7Padding(PKCS5Padding) 加密解密
iv是空的16字节数据
'''
iv = bytes(16)


def encrypt(data, key):
    if not isinstance(data, bytes):
        data = data.encode('utf-8')
    cipher_text = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv).encrypt(_pkcs7_padding(data))
    return base64.b64encode(cipher_text).decode('utf-8')


def decrypt(data, key):
    if not isinstance(data, bytes):
        data = data.encode('utf-8')
    plain_text = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv).decrypt(base64.b64decode(data))
    return bytes.decode(plain_text).rstrip("\x01"). \
        rstrip("\x02").rstrip("\x03").rstrip("\x04").rstrip("\x05"). \
        rstrip("\x06").rstrip("\x07").rstrip("\x08").rstrip("\x09"). \
        rstrip("\x0a").rstrip("\x0b").rstrip("\x0c").rstrip("\x0d"). \
        rstrip("\x0e").rstrip("\x0f").rstrip("\x10")


def _pkcs7_padding(data):
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    return padder.update(data) + padder.finalize()
