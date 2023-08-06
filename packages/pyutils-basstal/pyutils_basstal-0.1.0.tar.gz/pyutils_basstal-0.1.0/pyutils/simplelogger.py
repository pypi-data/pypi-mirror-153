import os
import sys

import pyutils.shorthand as shd

######################
######################
#       Log          #
######################
######################

LOG_LEVEL = None
LOG_LEVEL_NORMAL = 0
LOG_LEVEL_INFO = 1
LOG_LEVEL_WARNING = 2
LOG_LEVEL_ERROR = 3
LOG_LEVEL_SUCCESS = 4
LOG_LEVEL_NONE = 99
LOG_INDENT = 0
ErrorRaiseExcpetion = False

def color_message(message, color_code, bold=False):
    if shd.is_win():
        os.system('')
    result = '\033[{}m{}\033[0m'.format(color_code, message)
    if bold:
        result = '\033[1m' + result
    return result


def log(message, level=LOG_LEVEL_NORMAL, noident=False, bold=False):
    global LOG_INDENT, LOG_LEVEL

    if LOG_LEVEL is None:
        LOG_LEVEL = int(os.getenv('LoggerLevel', -1))

    if level >= LOG_LEVEL:
        if level == LOG_LEVEL_INFO:
            message = color_message(message, 34, bold)

        if level == LOG_LEVEL_WARNING:
            message = color_message('warning: {}'.format(message), 33, bold)

        if level == LOG_LEVEL_ERROR:
            message = color_message('error: {}'.format(message), 31, bold)

        if level == LOG_LEVEL_SUCCESS:
            message = color_message('success: {}'.format(message), 32, bold)

        if not shd.is_win():
            message = message.replace('=>', '➜').replace('<=', '✔')

        message += '\n'

        pipe = sys.stdout if level == LOG_LEVEL_NORMAL else sys.stderr

        pipe.write(('' if noident else ('\t' * LOG_INDENT)) + message)


def info(message, bold=False):
    log(message, LOG_LEVEL_INFO, False, bold)


def warning(message, bold=False):
    log(message, LOG_LEVEL_WARNING, False, bold)


def error(message, bold=False):
    if ErrorRaiseExcpetion:
        raise Exception(message)
    log(message, LOG_LEVEL_ERROR, False, bold)