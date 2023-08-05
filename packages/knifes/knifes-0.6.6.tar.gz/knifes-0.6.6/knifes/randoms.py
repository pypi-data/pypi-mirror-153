import random
import string
from knifes.digests import md5
from knifes import times
import uuid

id_alphabet = string.ascii_uppercase + string.digits


def random_str(length=4):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


# 16位唯一的
def make_unique_str():
    return md5(str(uuid.uuid1()))


# 碰撞概率极小的(唯一的)随机ID
# 建议长度 >= 10
def random_str_id(length=10):
    id = get_short_code_from_num(times.current_milli_time())
    if len(id) < length:
        return ''.join(random.choices(id_alphabet, k=length - len(id))) + id
    elif len(id) > length:
        return id[0:length]
    else:
        return id


def get_short_code_from_num(num):
    code = ''
    while num > 0:
        index = num % 36
        num = (num - index) // 36
        code = id_alphabet[index] + code
    return code
