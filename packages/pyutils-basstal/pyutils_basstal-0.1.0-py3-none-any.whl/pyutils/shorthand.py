import os
import sys

######################
######################
#       操作系统      #
######################
######################



def is_win():
    return sys.platform.lower().startswith('win')


def is_macOS():
    return sys.platform.lower().startswith('darwin')
