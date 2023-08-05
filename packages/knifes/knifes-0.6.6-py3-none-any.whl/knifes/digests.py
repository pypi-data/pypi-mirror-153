import base64
import hashlib


def b64encode(content):
    return base64.b64encode(content.encode('utf-8')).decode('utf-8')


def b64decode(content):
    return base64.b64decode(content.encode('utf-8')).decode('utf-8')


def b32encode(content):
    return base64.b32encode(content.encode('utf-8')).decode('utf-8')


def b32decode(content):
    return base64.b32decode(content.encode('utf-8')).decode('utf-8')


def md5(content):
    return hashlib.md5(content.encode()).hexdigest()