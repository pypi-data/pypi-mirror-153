import os


# 读文件
def read_file(filename, mode='r'):
    if not os.path.exists(filename):
        return ''
    fp = open(filename, mode)
    f_body = fp.read()
    fp.close()
    return f_body
