import subprocess


# cmd可传数组或者字符串，如: ['ls', '-al'] 或 'ls -al'
def exec_shell(cmd):
    ret = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return ret.stdout.decode('utf-8').strip(), ret.stderr.decode('utf-8').strip()


def print_succ(content):  # 绿色
    print('\033[32m{}\033[0m'.format(content))


def print_err(content):  # 红色
    print('\033[31m{}\033[0m'.format(content))