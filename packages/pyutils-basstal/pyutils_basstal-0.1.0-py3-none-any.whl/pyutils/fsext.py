import ctypes
import fnmatch
import glob
import os
import shutil

import pyutils.shorthand as shd
import pyutils.simplelogger as logger
########################
########################
#    文件系统扩展方法    #
########################
########################


def search(pattern:str, validator=None, params={}):
    """按指定路径模式搜索单路径，可以添加自定义验证函数来过滤匹配的路径

    Args:
        pattern (str): 路径匹配模式，在 windows 下会自动搜索所有盘符
        validator (function, optional): 自定义验证函数，回调参数为匹配的路径和 params. Defaults to None.
        params (dict, optional): 自定义验证函数的剩余回调参数. Defaults to {}.

    Returns:
        str | None: 搜索到的路径，未搜索到则返回 None
    """
    def glob_wrap(path):
        logger.info('=> Searching at {}'.format(path), False)
        result = glob.glob(path, recursive=True)
        if len(result) > 0:
            for find_path in result:
                if validator is None or validator(find_path, **params):
                    return find_path
    if shd.is_win():
        volumes = get_all_volumes_win()
        for volume in volumes:
            search_path = os.path.join(volume, pattern)
            result = glob_wrap(search_path)
            if result is not None:
                return result
    else:
        return glob_wrap(pattern)


def copy_files(target_path, src_file_list):
    for src_file in src_file_list:
        if os.path.exists(src_file):
            src_basename = os.path.basename(src_file)
            deploy_file_path = os.path.join(target_path, src_basename)
            deploy_dir = os.path.dirname(deploy_file_path)
            if not os.path.exists(deploy_dir):
                os.makedirs(deploy_dir)
                logger.info('Makedirs => {}'.format(deploy_dir))
            if os.path.isfile(deploy_file_path):
                os.remove(deploy_file_path)
                logger.info('Removed => {}'.format(deploy_file_path))

            shutil.copy(src_file, deploy_file_path)
            logger.info('Copy file from {} to => {}'.format(src_file, deploy_file_path))


def read_file(file, decode='utf-8'):
    if os.path.isfile(file):
        content = ''
        with open(file, 'rb') as fo:
            content = fo.read()
        content = content.decode(decode)
        return content
    else:
        logger.error('{} is not found or is not a file'.format(file))


def get_all_volumes_win():
    if shd.is_win():
        lp_buffer = ctypes.create_string_buffer(78)
        ctypes.windll.kernel32.GetLogicalDriveStringsA(
            ctypes.sizeof(lp_buffer), lp_buffer)
        all_volumes = lp_buffer.raw.split(b'\x00')
        legal_volumes = []
        for vol in all_volumes:
            s = str(vol, encoding='utf-8')
            if os.path.isdir(s):
                legal_volumes.append(s)
        return legal_volumes


def get_files(work_dir, include_patterns=None, ignore_patterns=None, follow_links=False, recursive=True, apply_ignore_when_conflick=True):
    """
    NOTE:这里的 patterns 用的是 UNIX 通配符，而非语言正则表达式
    """
    if os.path.isfile(work_dir):
        result = [work_dir]
    else:
        result = []
        walk_result = os.walk(work_dir, followlinks=follow_links)
        if not recursive:
            try:
                walk_result = [next(walk_result)]
            except:
                walk_result = None
        if walk_result is not None:
            for dirpath, _, filenames in walk_result:
                for filename in filenames:
                    full_path = os.path.join(dirpath, filename)
                    valid = True
                    if ignore_patterns is not None:
                        for ignore_pattern in ignore_patterns:
                            match_result = fnmatch.fnmatch(full_path, ignore_pattern)
                            valid = valid and not match_result
                            if not valid:
                                break
                    if include_patterns is not None:
                        for include_pattern in include_patterns:
                            match_result = fnmatch.fnmatch(full_path, include_pattern)
                            if apply_ignore_when_conflick:
                                valid = match_result and valid
                            else:
                                valid = match_result or valid
                            if valid:
                                break
                    if valid:
                        result.append(full_path)
    return sorted(result)

