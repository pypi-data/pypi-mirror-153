import os
import tempfile
import time
import subprocess
import sys
import charade
import fsext

import pyutils.simplelogger as logger
import pyutils.shorthand as shd

def detect_encoding(input):
    """
    猜测 bytes | str 的编码

    Args:
        input (str | bytes): 待猜测的内容
    """
    try:
        # check it in the charade list
        if isinstance(input, str):
            return charade.detect(input.encode())
        # detecting the string
        else:
            return charade.detect(input)
    # in case of error
    # encode with 'utf -8' encoding
    except UnicodeDecodeError:
        return charade.detect(input.encode('utf-8'))


######################
######################
#   执行脚本or模块    #
######################
######################


class ExecuteResult:
    def __init__(self):
        self.cmd_line = None
        self.code = 0
        self.out = None
        self.error = None
        self.exception = None
        self.out_str = None


class Executor:

    verbose = True

    def __init__(self, verbose=True):
        self.verbose = verbose

    def format_args(self, args):
        if type(args) is list:
            return ' '.join(args)
        elif type(args) is str:
            return args
        elif args is not None:
            logger.info('Unsupported args type : {}'.format(type(args)))
        return ' '

    def common_error_out(self, result, exit_code=-1):
        """
        输出错误信息的

        Args:
            result ([class ExecuteResult]): 收集的执行结果
            exit_code (number, optional): sys.exit() 参数. Defaults to -1
        """
        error_message = f'{result.error}\n{result.out_str}' if result.error != '' else result.out_str
        logger.error(f'\nCommand failed: {result.cmd_line}\n'
                f'code: {result.code}\n'
                f'message: {error_message}', True)
        sys.exit(exit_code)

    def path_to_temp_dir(self):
        """
        获得（且创建）临时文件夹地址

        Returns:
            string: 临时文件夹地址
        """
        dir = os.path.join(os.getcwd(), '.temp')
        if not os.path.exists(dir):
            os.mkdir(dir)
        return dir

    def execute_by_git_bash(self, cmd, args, ignore_error=False, use_direct_stdout=False, exit_at_once=False, env=None, shell=True):
        """
        将待执行的命令（ cmd 和 args ）写入临时文件中，
        通过 git-bash 程序来运行该临时文件，
        这是为了解决 windows cmd 对某些特殊字符处理错误的问题。

        Args:
            cmd (str): 命令
            args (list or str): 参数列表
            ignore_error (bool, optional): 是否忽略报错. Defaults to False.
            use_direct_stdout (bool, optional): 是否将输出接到 sys.stdout . Defaults to False.
            exit_at_once (bool, optional): 是否在进程开启后直接返回. Defaults to False.
            env (str, optional): Popen env argument. Defaults to None.
            shell (bool, optional): Popen shell argument. Defaults to True.
        """
        
        tf= tempfile.mkstemp(suffix='.sh', prefix=None, dir=self.path_to_temp_dir(), text=True)
        args = self.format_args(args)
        cmd_line = '{0} {1}'.format(cmd, args)
        with open(tf[1], 'w+') as f:
            f.write(cmd_line)
        result = self.execute_file(tf[1], None, ignore_error=ignore_error, use_direct_stdout=use_direct_stdout, exit_at_once=exit_at_once, env=env, shell=shell)
        os.close(tf[0])
        os.unlink(tf[1])
        return result

    def execute_straight(self, cmd, args, ignore_error=False, use_direct_stdout=False, exit_at_once=False, env=None, shell=True):
        """
        启动subprocess , 直接执行命令

        @cmd
            命令
        @args
            可以是 dict 参数列表也可以直接是 str 参数
        @ignore_error
            忽略遇到的错误继续执行，否则会遇到错误会调用 sys.exit(-1)
        @use_direct_stdout
            是否使用 sys.stdout 作为输出
        @exit_at_once
            是否直接返回，否则同步等待命令结束
        @env
            Popen env argument
        @shell
            Popen shell argument
        """
        args = self.format_args(args)
        cmd_line = '{0} {1}'.format(cmd, args)

        if self.verbose:
            logger.LOG_INDENT
            logger.LOG_INDENT += 1
            logger.info('=> Shell: {}'.format(cmd_line), True)

        start_time = time.time()
        pipes = subprocess.Popen(cmd_line, stdout=sys.stdout if use_direct_stdout else subprocess.PIPE,
                                 stderr=subprocess.PIPE, env=env, shell=shell)
        result = ExecuteResult()
        result.cmd_line = cmd_line
        if exit_at_once:
            result.code = 0
        else:
            result.out, result.error = pipes.communicate()
            result.out = "" if result.out is None else result.out.strip()
            error_encoding = detect_encoding(result.error)['encoding']
            result.error = "" if result.error is None else str(result.error.strip(), error_encoding if error_encoding is not None else 'utf-8')
            result.code = pipes.returncode
            out_encoding = detect_encoding(result.out)['encoding']
            result.out_str = result.out if isinstance(result.out, str) else str(result.out, out_encoding if out_encoding is not None else 'utf-8')
        if self.verbose:
            logger.info('<= Finished: {0} {1:.2f} seconds'.format(
                os.path.basename(cmd), time.time() - start_time), True)

        if not ignore_error and result.code != 0:
            self.common_error_out(result)
        if self.verbose:
            logger.LOG_INDENT -= 1
        return result

    # https://blog.csdn.net/doots/article/details/86705182
    SET_ENV = r'''
    @echo off
    set %{key}%={value}

    if {user}==sys (
        setx /M {key} "{value}"
    ) else (
        setx {key} "{value}"
    )
    '''

    ADD_ENV = r'''
    @echo off

    if {user}==sys (
        set regPath= HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session" "Manager\Environment
    ) else (
        set regPath= HKEY_CURRENT_USER\Environment
    )

    set key={key}
    set value={value}
    :: 判断是否存在该路径
    reg query %regPath% /v %key% 1>nul 2>nul
    if %ERRORLEVEL%==0 (
        :: 取值
        For /f "tokens=3* delims= " %%i in ('Reg Query %regPath% /v %key% ') do (
            if "%%j"=="" (Set oldValue=%%i) else (Set oldValue=%%i %%j)
        )
    ) else Set oldValue=

    :: 备份注册表
    @REM reg export %regPath% %~dp0%~n0.reg
    :: 写入环境变量
    if "%oldValue%"=="" (
        reg add %regPath% /v %key% /t REG_EXPAND_SZ /d "%value%" /f
    ) else (
        if {override}==True (
            reg add %regPath% /v %key% /t REG_EXPAND_SZ /d "%value%" /f
        ) else (
            reg add %regPath% /v %key% /t REG_EXPAND_SZ /d "%oldValue%;%value%" /f
        )
    )
    '''


    def set_env_win(self, key:str, value:str, override=False):
        """
        windows 设置系统环境变量
        使用生成 bat 文件并执行的方式

        Args:
            key (str): 环境变量的键
            value (str): 环境变量的值
            override (bool, optional): 如果环境变量已存在，是否采用覆盖的方式. Defaults to False.
        """
        if not shd.is_win():
            logger.error('set_env_win failed! your OS is not windows.')
            return
        if value[-1] == '\\':
            value = value[:-1] + '/'
        # 运行设置环境变量命令
        bat_cmd = self.ADD_ENV.format(user='me', key=key, value=value, override=override)
        # info('=> run cmd : \n {}'.format(bat_cmd))
        tf= tempfile.mkstemp(suffix='.bat', prefix=None, dir=self.path_to_temp_dir(), text=True)
        with open(tf[1], 'w+', encoding='utf-8') as f:
            f.write(bat_cmd)
        self.execute_file(tf[1], None)
        os.close(tf[0])
        os.unlink(tf[1])
        if override:
            logger.info('=> Set system environment {0}={1} finished.'.format(key, value))
        else:
            logger.info('=> Append {1} to system environment key {0}.'.format(key, value))
            
    def get_git_path(self):
        """
        先尝试从环境变量获取，如果失败则搜索本地路径以获取 git 安装路径

        Args:
            executor ([class Executor]): 执行 git-bash 的终端接口
        """
        git_path = os.getenv('GIT_PATH')

        if git_path == None:
            logger.warning('=> Begin searching git path, it will take a long time...', False)
            # windows 先搜索默认路径
            if shd.is_win():
                git_path = fsext.search('/Program*/Git/git-bash.exe')
                if git_path == None:
                    git_path = fsext.search('/**/Git/git-bash.exe')
                if git_path != None:
                    git_path = git_path.replace('git-bash.exe', '')
                    self.set_env_win('GIT_PATH', git_path, override=True)
            # TODO: 目前 macOS 搜索路径是写死的
            elif shd.is_macOS():
                git_path = fsext.search('/usr/bin/git')

        if git_path == None:
            logger.error('=> Cannot find git install path. ??')
            exit(-2)
        return git_path

    def ext_to_exe(self, ext):
        """
        按传入的后缀名称选择对应的可执行程序

        Args:
            ext (str): 待执行文件后缀
        """
        if ext.endswith('.sh'):
            if shd.is_win():
                # NOTE:windows调用sh
                return '"{}"'.format(os.path.join(self.get_git_path(), 'usr/bin/bash.exe'))
            else:
                return '/bin/bash'
        if ext.endswith('.py'):
            return 'python'

    def execute_file(self, script, args, work_dir=None, ignore_error=False, use_direct_stdout=False, exit_at_once=False, env=None, shell=True):
        """
        执行脚本文件并传入参数

        Args:
            script (str): 脚本文件路径
            args (list or str): 参数
            work_dir (str, optional): 工作目录. Defaults to None.
            ignore_error (bool, optional): 是否忽略执行过程中的报错. Defaults to False.
            use_direct_stdout (bool, optional): 是否使用 sys.stdout 作为输出流. Defaults to False.
            exit_at_once (bool, optional): 是否异步执行. Defaults to False.
            env (dict, optional): 传入给 popen 的 env. Defaults to None.
            shell (bool, optional): 传入给 popen 的 shell. Defaults to True.

        Returns:
            [type]: [description]
        """
        args = self.format_args(args)
        previous_cwd = os.getcwd()
        if work_dir is not None:
            # should be restore
            os.chdir(os.path.realpath(work_dir))

        split_result = os.path.splitext(script)
        result = None
        exe = self.ext_to_exe(split_result[1])
        if exe is None:
            result = self.execute_straight(
                script, args, ignore_error, use_direct_stdout, exit_at_once, env, shell)
        else:
            result = self.execute_straight(
                f'{exe} {script}', args, ignore_error, use_direct_stdout, exit_at_once, env, shell)

        os.chdir(previous_cwd)
        return result

    def execute_module(self, module, *module_parameters):
        logger.LOG_INDENT += 1

        module_name = module.__name__
        logger.info('=> Module: {}'.format(module_name), True)
        start_time = time.time()
        result = module.main(*module_parameters)
        logger.info('<= Finished: {0} {1:.2f} seconds '.format(module_name, time.time() - start_time), True)

        logger.LOG_INDENT -= 1
        return result
