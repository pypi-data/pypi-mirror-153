# Created by Q-ays.
# whosqays@gmail.com


import os
from wisdoms.commons import my_code as codes

SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

revert = codes.revert
codes = codes


ABC_KEYS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "M", "L", "N", "O", "P", "Q", "R", "S", "T", "U",
            "V", "W", "X", "Y", "Z"]


def success(data=None):
    """
    封装revert方法，返回执行成功code

    :param data:
    :return:
    """
    return revert(codes.SUCCESS, data)
