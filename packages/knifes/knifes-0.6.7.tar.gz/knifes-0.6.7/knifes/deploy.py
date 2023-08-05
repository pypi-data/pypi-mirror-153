from .shell import *
from .file import read_file
import time
import sys
from datetime import datetime, timedelta


def print_help(project_dir):
    print('deploy   --install modules and reload gunicorn\n'
          'reload   --reload gunicorn\n'
          'modules  --install modules\n'
          'log n    --read gunicorn last log\n'
          'start    --start gunicorn\n'
          'knifes   --force install latest knifes\n\n'
          'activate virtual environment cmd:\n\n'
          'source {}venv/bin/activate'.format(project_dir))


def main_script(chdir, logdir, project_name, app_name=None):
    args = sys.argv[1:]
    if not args:
        print_help(chdir)
    elif args[0] == 'reload':
        reload_gunicorn(logdir)
    elif args[0] == 'modules':
        install_modules(chdir)
    elif args[0] == 'log':
        line_count = 10 if len(args) == 1 else args[1]
        read_last_log(logdir, line_count)
    elif args[0] == 'deploy':
        install_modules(chdir)
        reload_gunicorn(logdir)
    elif args[0] == 'start':
        start_gunicorn(chdir, logdir, project_name, app_name)
    elif args[0] == 'knifes':
        install_latest_knifes(chdir)
    else:
        print_help(chdir)


def install_latest_knifes(project_dir):
    cmd = 'source {}venv/bin/activate && pip install knifes --index-url https://pypi.python.org/simple -U'.format(project_dir)
    succ, err = exec_shell(cmd)
    print_succ(succ)
    print_err(err)


def install_modules(project_dir):
    cmd = 'source {}venv/bin/activate && pip install -r {}requirements.txt'.format(project_dir, project_dir)
    succ, err = exec_shell(cmd)
    print_succ(succ)
    print_err(err)


def read_last_log(log_dir, line_count):
    succ, err = exec_shell('tail -{} {}error.log'.format(line_count, log_dir))
    print_succ(succ)
    print_err(err)
    return succ, err


def start_gunicorn(project_dir, log_dir, project_name, app_name=None):
    if not app_name:
        app_name = project_name
    """
    调用前先在project目录下创建venv环境,如:
    /root/.pyenv/versions/3.7.2/bin/python -m venv venv
    """
    cmd = '{}venv/bin/gunicorn -c {}gunicorn_{}_conf.py {}.wsgi:application'.format(project_dir, project_dir, app_name, project_name)
    # 判断是否已启动
    succ, err = exec_shell("pgrep -f '{}'".format(cmd))
    if succ:
        print_err('当前已启动！请通过reload命令重启')
        return

    succ, err = exec_shell(cmd)
    print_succ(succ)
    print_err(err)
    time.sleep(1)
    read_last_log(log_dir, 6)


def reload_gunicorn(log_dir):
    pid_filename = '{}pid.pid'.format(log_dir)
    pid = read_file(pid_filename).strip()
    print('gunicorn pid:{}'.format(pid))
    if not pid:
        print_err('重启gunicorn失败,pid不存在:{}'.format(pid_filename))
    exec_shell('kill -HUP {}'.format(pid))
    time.sleep(1)
    succ, err = read_last_log(log_dir, 6)
    if not succ:
        print_err('重启失败！重启失败！重启失败！')
        return
    # 判断时间是不是2s内
    line = next(filter(lambda x: 'Hang up: Master' in x, succ.split('\n')), None)
    if not line:
        print_err('重启失败！重启失败！重启失败！')
        return
    if datetime.strptime(line[1:20], '%Y-%m-%d %H:%M:%S') > (datetime.now() - timedelta(seconds=3)):
        print_succ('重启成功:{}'.format(line[1:20]))
    else:
        print_err('重启失败！重启失败！重启失败！')